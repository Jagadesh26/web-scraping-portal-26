import logging
import os
import re
import tempfile
from datetime import date
from decimal import Decimal

from django.db import transaction

from apps.resumes.models import (
    ResumeAnalysis,
    ResumeEducation,
    ResumeExperience,
    ResumeProject,
    ResumeRecommendation,
    ResumeSkill,
)
from apps.resumes.parsers.parser_factory import ParserFactory
from apps.resumes.services.education_extractor_service import (
    EducationExtractorService
)
from apps.resumes.services.experience_extractor_service import (
    ExperienceExtractorService
)
from apps.resumes.services.project_extractor_service import (
    ProjectExtractorService
)
from apps.resumes.services.section_detector_service import (
    SectionDetectorService
)
from apps.resumes.services.skill_extractor_service import (
    SkillExtractorService
)

logger = logging.getLogger(__name__)


class ResumeAnalysisService:

    TARGET_SKILLS = {
        "Python",
        "Django",
        "PostgreSQL",
        "Docker",
        "Redis",
        "Kafka",
        "AWS",
    }

    @classmethod
    def process_resume(
        cls,
        resume,
        resume_file
    ):
        resume.status = "PROCESSING"
        resume.save(
            update_fields=["status"]
        )

        temp_path = None

        try:
            temp_path = cls.create_temp_file(
                resume,
                resume_file
            )
            raw_text = cls.extract_text(
                resume,
                temp_path
            )
            sections = SectionDetectorService.detect_sections(
                raw_text
            )

            with transaction.atomic():
                cls.clear_previous_results(
                    resume
                )

                skills = SkillExtractorService.extract_skills(
                    resume=resume,
                    raw_text=sections.get("skills") or raw_text
                )
                experiences = ExperienceExtractorService.extract_experience(
                    resume=resume,
                    raw_text=sections.get("experience") or raw_text
                )
                educations = EducationExtractorService.extract_education(
                    resume=resume,
                    raw_text=sections.get("education") or raw_text
                )
                projects = ProjectExtractorService.extract_projects(
                    resume=resume,
                    raw_text=sections.get("projects") or raw_text
                )

                total_experience = cls.calculate_total_experience(
                    experiences
                )
                scores = cls.calculate_scores(
                    raw_text=raw_text,
                    skills=skills,
                    experiences=experiences,
                    educations=educations,
                    projects=projects,
                )

                analysis = ResumeAnalysis.objects.create(
                    resume=resume,
                    raw_text=raw_text,
                    summary=cls.build_summary(
                        skills,
                        experiences,
                        educations,
                        projects
                    ),
                    total_experience=total_experience,
                    current_designation=cls.get_current_designation(
                        experiences
                    ),
                    **scores
                )

                cls.create_recommendations(
                    resume=resume,
                    raw_text=raw_text,
                    skills=skills,
                    experiences=experiences,
                    educations=educations,
                    projects=projects,
                )

                resume.status = "COMPLETED"
                resume.save(
                    update_fields=["status"]
                )

                from apps.ats.tasks import process_resume_jobs_task

                transaction.on_commit(
                    lambda: process_resume_jobs_task.delay(
                        str(resume.id)
                    ),
                    robust=True
                )

            return analysis

        except Exception:
            logger.exception(
                "Resume processing failed: %s",
                resume.id
            )
            resume.status = "FAILED"
            resume.save(
                update_fields=["status"]
            )
            return None

        finally:
            if temp_path and os.path.exists(
                temp_path
            ):
                os.unlink(
                    temp_path
                )

    @staticmethod
    def create_temp_file(
        resume,
        resume_file
    ):
        if hasattr(
            resume_file,
            "seek"
        ):
            resume_file.seek(
                0
            )

        suffix = f".{resume.file_type.lower()}"
        temp_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        )

        try:
            if hasattr(
                resume_file,
                "chunks"
            ):
                for chunk in resume_file.chunks():
                    temp_file.write(
                        chunk
                    )
            else:
                temp_file.write(
                    resume_file.read()
                )
        finally:
            temp_file.close()

        if hasattr(
            resume_file,
            "seek"
        ):
            resume_file.seek(
                0
            )

        return temp_file.name

    @staticmethod
    def extract_text(
        resume,
        file_path
    ):
        parser = ParserFactory.get_parser(
            resume.file_type
        )

        return parser.extract_text(
            file_path
        )

    @staticmethod
    def clear_previous_results(
        resume
    ):
        ResumeAnalysis.objects.filter(
            resume=resume
        ).delete()
        ResumeSkill.objects.filter(
            resume=resume
        ).delete()
        ResumeExperience.objects.filter(
            resume=resume
        ).delete()
        ResumeEducation.objects.filter(
            resume=resume
        ).delete()
        ResumeProject.objects.filter(
            resume=resume
        ).delete()
        ResumeRecommendation.objects.filter(
            resume=resume
        ).delete()

    @staticmethod
    def calculate_total_experience(
        experiences
    ):
        total = sum(
            Decimal(
                str(
                    experience.years_of_experience or 0
                )
            )
            for experience in experiences
        )

        return total.quantize(
            Decimal("0.1")
        )

    @classmethod
    def calculate_scores(
        cls,
        raw_text,
        skills,
        experiences,
        educations,
        projects
    ):
        skills_score = min(
            len(skills) * 12.5,
            100
        )
        total_experience = sum(
            float(
                experience.years_of_experience or 0
            )
            for experience in experiences
        )

        if total_experience >= 5:
            experience_score = 100
        elif total_experience >= 3:
            experience_score = 80
        elif total_experience >= 1:
            experience_score = 60
        elif experiences:
            experience_score = 45
        else:
            experience_score = 0

        education_score = 0
        if educations:
            best = max(
                (
                    50
                    + (20 if education.institution else 0)
                    + (15 if education.start_year else 0)
                    + (15 if education.end_year else 0)
                    for education in educations
                ),
                default=0
            )
            education_score = min(
                best,
                100
            )

        project_score = min(
            len(projects) * 35,
            100
        )

        skill_set = {
            skill.lower()
            for skill in skills
        }
        keyword_score = round(
            len(
                {
                    skill
                    for skill in cls.TARGET_SKILLS
                    if skill.lower() in skill_set
                }
            )
            / len(cls.TARGET_SKILLS)
            * 100,
            2
        )
        completeness_score = cls.calculate_completeness_score(
            raw_text,
            skills,
            experiences,
            educations,
            projects
        )

        overall_score = (
            Decimal(str(skills_score)) * Decimal("0.30")
            + Decimal(str(experience_score)) * Decimal("0.25")
            + Decimal(str(education_score)) * Decimal("0.15")
            + Decimal(str(project_score)) * Decimal("0.15")
            + Decimal(str(keyword_score)) * Decimal("0.15")
        )

        return {
            "overall_score": overall_score.quantize(
                Decimal("0.01")
            ),
            "skills_score": Decimal(str(skills_score)).quantize(
                Decimal("0.01")
            ),
            "experience_score": Decimal(str(experience_score)).quantize(
                Decimal("0.01")
            ),
            "education_score": Decimal(str(education_score)).quantize(
                Decimal("0.01")
            ),
            "project_score": Decimal(str(project_score)).quantize(
                Decimal("0.01")
            ),
            "keyword_score": Decimal(str(keyword_score)).quantize(
                Decimal("0.01")
            ),
            "completeness_score": Decimal(str(completeness_score)).quantize(
                Decimal("0.01")
            ),
        }

    @staticmethod
    def calculate_completeness_score(
        raw_text,
        skills,
        experiences,
        educations,
        projects
    ):
        checks = [
            bool(skills),
            bool(experiences),
            bool(educations),
            bool(projects),
            bool(
                re.search(
                    r"[\w.+-]+@[\w-]+\.[\w.-]+",
                    raw_text
                )
            ),
            bool(
                re.search(
                    r"(?:\+?\d[\d\s-]{8,}\d)",
                    raw_text
                )
            ),
        ]

        return round(
            sum(checks) / len(checks) * 100,
            2
        )

    @staticmethod
    def build_summary(
        skills,
        experiences,
        educations,
        projects
    ):
        return (
            f"Extracted {len(skills)} skills, "
            f"{len(experiences)} experience entries, "
            f"{len(educations)} education entries, "
            f"and {len(projects)} projects."
        )

    @staticmethod
    def get_current_designation(
        experiences
    ):
        if not experiences:
            return ""

        latest = sorted(
            experiences,
            key=lambda item: item.end_date or item.start_date or date.min,
            reverse=True
        )[0]

        return latest.designation

    @classmethod
    def create_recommendations(
        cls,
        resume,
        raw_text,
        skills,
        experiences,
        educations,
        projects
    ):
        recommendations = []
        skill_set = {
            skill.lower()
            for skill in skills
        }
        missing_skills = [
            skill
            for skill in sorted(
                cls.TARGET_SKILLS
            )
            if skill.lower() not in skill_set
        ]

        if missing_skills:
            recommendations.append(
                (
                    "Missing Skills",
                    "Add these market-relevant skills if you have experience with them: "
                    + ", ".join(missing_skills)
                )
            )

        if not experiences:
            recommendations.append(
                (
                    "Experience",
                    "Add company, designation, dates, and measurable impact for each role."
                )
            )

        if not projects:
            recommendations.append(
                (
                    "Projects",
                    "Add project names, descriptions, and technologies used."
                )
            )

        if not educations or any(
            not education.institution or not education.end_year
            for education in educations
        ):
            recommendations.append(
                (
                    "Education",
                    "Add degree, institution, and start/end year details."
                )
            )

        if not re.search(
            r"[\w.+-]+@[\w-]+\.[\w.-]+",
            raw_text
        ) or not re.search(
            r"(?:\+?\d[\d\s-]{8,}\d)",
            raw_text
        ):
            recommendations.append(
                (
                    "Contact",
                    "Add clear contact information including email and phone number."
                )
            )

        ResumeRecommendation.objects.bulk_create(
            [
                ResumeRecommendation(
                    resume=resume,
                    category=category,
                    recommendation=recommendation
                )
                for category, recommendation in recommendations
            ]
        )
