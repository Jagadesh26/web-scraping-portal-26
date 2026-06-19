from decimal import Decimal

from apps.jobs.models import JobMatch
from apps.resumes.models import (
    ResumeAnalysis,
    ResumeEducation,
    ResumeProject,
    ResumeSkill,
)


class ATSMatchingService:

    WEIGHTS = {
        "skill_score": Decimal("0.40"),
        "experience_score": Decimal("0.25"),
        "education_score": Decimal("0.15"),
        "project_score": Decimal("0.10"),
        "resume_quality_score": Decimal("0.10"),
    }

    @classmethod
    def calculate(
        cls,
        user,
        job
    ):
        resume = (
            getattr(
                user,
                "resume",
                None
            )
        )

        if not resume:
            return None

        skill_result = cls.calculate_skill_match(
            resume,
            job
        )
        skill_score = Decimal(
            str(skill_result["score"])
        )
        experience_score = Decimal(
            str(
                cls.calculate_experience_match(
                    resume,
                    job
                )
            )
        )
        education_score = Decimal(
            str(
                cls.calculate_education_match(
                    resume,
                    job
                )
            )
        )
        project_score = Decimal(
            str(
                cls.calculate_project_match(
                    resume,
                    job,
                    skill_result["job_skills"]
                )
            )
        )
        resume_quality_score = Decimal(
            str(
                cls.calculate_resume_quality_score(
                    resume
                )
            )
        )

        final_score = sum(
            {
                "skill_score": skill_score,
                "experience_score": experience_score,
                "education_score": education_score,
                "project_score": project_score,
                "resume_quality_score": resume_quality_score,
            }[name] * weight
            for name, weight in cls.WEIGHTS.items()
        ).quantize(
            Decimal("0.01")
        )
        recommendations = cls.generate_recommendations(
            skill_result["missing_skills"]
        )
        improvement_suggestions = cls.generate_improvement_suggestions(
            skill_score,
            experience_score,
            education_score,
            project_score,
            resume_quality_score,
        )

        job_match, _ = (
            JobMatch.objects.update_or_create(

                user=user,

                job=job,

                defaults={

                    "skill_score":
                        skill_score,

                    "experience_score":
                        experience_score,

                    "preference_score":
                        0,

                    "education_score":
                        education_score,

                    "project_score":
                        project_score,

                    "resume_quality_score":
                        resume_quality_score,

                    "location_score":
                        0,

                    "ai_score":
                        0,

                    "final_score":
                        final_score,

                    "matched_skills":
                        skill_result[
                            "matched_skills"
                        ],

                    "missing_skills":
                        skill_result[
                            "missing_skills"
                        ],

                    "recommendations":
                        recommendations,

                    "improvement_suggestions":
                        improvement_suggestions,

                    "match_category":
                        cls.get_match_category(
                            final_score
                        ),
                }
            )
        )

        return job_match

    @staticmethod
    def normalize_skill_names(
        values
    ):
        return {
            value.strip().lower()
            for value in values
            if value
        }

    @classmethod
    def calculate_skill_match(
        cls,
        resume,
        job
    ):
        resume_skills = cls.normalize_skill_names(
            ResumeSkill.objects.filter(
                resume=resume
            ).values_list(
                "skill__name",
                flat=True
            )
        )
        job_skills = cls.normalize_skill_names(
            job.job_skills.select_related(
                "skill"
            ).values_list(
                "skill__name",
                flat=True
            )
        )

        if not job_skills:
            return {
                "score": 0,
                "matched_skills": [],
                "missing_skills": [],
                "job_skills": set(),
            }

        matched_skills = sorted(
            resume_skills.intersection(
                job_skills
            )
        )
        missing_skills = sorted(
            job_skills - resume_skills
        )
        score = round(
            len(matched_skills) / len(job_skills) * 100,
            2
        )

        return {
            "score": score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "job_skills": job_skills,
        }

    @staticmethod
    def calculate_experience_match(
        resume,
        job
    ):
        analysis = ResumeAnalysis.objects.filter(
            resume=resume
        ).first()

        if not analysis:
            return 0

        user_experience = float(
            analysis.total_experience or 0
        )
        experience_min = float(
            job.experience_min or 0
        )
        experience_max = float(
            job.experience_max or 0
        )

        if experience_min == 0 and experience_max == 0:
            return 100

        if experience_min <= user_experience and (
            experience_max == 0 or user_experience <= experience_max
        ):
            return 100

        if user_experience < experience_min:
            if experience_min == 0:
                return 100

            return round(
                max(
                    user_experience / experience_min * 100,
                    40 if user_experience > 0 else 0
                ),
                2
            )

        return 80

    @classmethod
    def calculate_education_match(
        cls,
        resume,
        job
    ):
        resume_level = max(
            (
                cls.degree_level(
                    education.degree
                )
                for education in ResumeEducation.objects.filter(
                    resume=resume
                )
            ),
            default=0
        )
        required_level = cls.required_degree_level(
            f"{job.title} {job.description}"
        )

        if required_level == 0:
            return 100 if resume_level else 50

        if resume_level >= required_level:
            return 100

        if resume_level == 0:
            return 30

        return 60 if resume_level + 1 == required_level else 30

    @staticmethod
    def degree_level(
        degree
    ):
        value = (
            degree or ""
        ).lower()

        if any(
            token in value
            for token in ["phd", "ph.d", "doctor"]
        ):
            return 4

        if any(
            token in value
            for token in ["master", "m.tech", "m.e", "m.sc", "mca", "mba"]
        ):
            return 3

        if any(
            token in value
            for token in ["bachelor", "b.tech", "b.e", "b.sc", "bca"]
        ):
            return 2

        if "diploma" in value:
            return 1

        return 0

    @staticmethod
    def required_degree_level(
        text
    ):
        value = (
            text or ""
        ).lower()

        if any(
            token in value
            for token in ["phd", "ph.d", "doctor"]
        ):
            return 4

        if any(
            token in value
            for token in ["master", "mca", "m.tech", "mba"]
        ):
            return 3

        if any(
            token in value
            for token in ["bachelor", "b.tech", "b.e", "degree"]
        ):
            return 2

        return 0

    @classmethod
    def calculate_project_match(
        cls,
        resume,
        job,
        job_skills
    ):
        if not job_skills:
            return 0

        project_text = " ".join(
            f"{project.project_name} {project.description} {project.technologies}"
            for project in ResumeProject.objects.filter(
                resume=resume
            )
        )
        project_skills = {
            skill
            for skill in job_skills
            if skill in project_text.lower()
        }

        return round(
            len(project_skills) / len(job_skills) * 100,
            2
        )

    @staticmethod
    def calculate_resume_quality_score(
        resume
    ):
        analysis = ResumeAnalysis.objects.filter(
            resume=resume
        ).first()

        if not analysis:
            return 0

        return float(
            analysis.overall_score or analysis.completeness_score or 0
        )

    @staticmethod
    def get_match_category(
        score
    ):
        score = float(
            score
        )

        if score >= 90:
            return "Excellent Match"

        if score >= 75:
            return "Strong Match"

        if score >= 60:
            return "Good Match"

        if score >= 40:
            return "Average Match"

        return "Poor Match"

    @staticmethod
    def generate_recommendations(
        missing_skills
    ):
        return [
            f"Learn {skill.title()}"
            for skill in missing_skills
        ]

    @staticmethod
    def generate_improvement_suggestions(
        skill_score,
        experience_score,
        education_score,
        project_score,
        resume_quality_score
    ):
        suggestions = []

        if skill_score < 60:
            suggestions.append(
                "Add missing technologies from the job requirements."
            )

        if experience_score < 60:
            suggestions.append(
                "Add relevant experience with clear dates and measurable impact."
            )

        if education_score < 60:
            suggestions.append(
                "Add education details that match the role requirements."
            )

        if project_score < 60:
            suggestions.append(
                "Add technical projects using skills required by the job."
            )

        if resume_quality_score < 60:
            suggestions.append(
                "Improve resume structure, completeness, and keyword coverage."
            )

        return suggestions
