import logging

from django.db import transaction

from apps.resumes.models import (
    Resume,
    ResumeAnalysis,
    ResumeEducation,
    ResumeExperience,
    ResumeProject,
    ResumeSkill,
)

from apps.resumes.parsers.parser_factory import ParserFactory
from apps.resumes.services.education_extractor_service import (
    EducationExtractorService
)
from apps.resumes.services.section_detector_service import (
    SectionDetectorService
)

from apps.resumes.services.experience_extractor_service import (
    ExperienceExtractorService
)
from apps.resumes.services.project_extractor_service import (
    ProjectExtractorService
)
from apps.resumes.services.skill_extractor_service import (
    SkillExtractorService
)

logger = logging.getLogger(__name__)


class ResumeParserService:

    @staticmethod
    def parse_resume(
        resume: Resume,
        file_path: str
    ):

        try:

            resume.status = "PROCESSING"
            resume.save(
                update_fields=["status"]
            )

            parser = (
                ParserFactory.get_parser(
                    resume.file_type
                )
            )

            raw_text = (
                parser.extract_text(
                    file_path
                )
            )

            sections = (
                SectionDetectorService.detect_sections(
                    raw_text
                )
            )

            with transaction.atomic():

                analysis, _ = (
                    ResumeAnalysis.objects.get_or_create(
                        resume=resume
                    )
                )

                analysis.raw_text = raw_text

                analysis.save()

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

                SkillExtractorService.extract_skills(
                    resume=resume,
                    raw_text=sections.get("skills") or raw_text
                )

                ExperienceExtractorService.extract_experience(
                    resume=resume,
                    raw_text=sections.get("experience") or raw_text
                )

                EducationExtractorService.extract_education(
                    resume=resume,
                    raw_text=sections.get("education") or raw_text
                )

                ProjectExtractorService.extract_projects(
                    resume=resume,
                    raw_text=sections.get("projects") or raw_text
                )

                resume.status = "COMPLETED"

                resume.save(
                    update_fields=["status"]
                )

            return analysis

        except Exception:

            logger.exception(
                f"Resume parsing failed: {resume.id}"
            )

            resume.status = "FAILED"

            resume.save(
                update_fields=["status"]
            )

            raise
