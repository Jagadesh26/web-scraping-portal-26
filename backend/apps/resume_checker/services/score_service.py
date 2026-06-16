from decimal import Decimal

from django.db import transaction

from apps.resume_checker.models import ResumeScore
from apps.resume_checker.services.experience_analyzer import ResumeExperienceAnalyzer
from apps.resume_checker.services.keyword_analyzer import ResumeKeywordAnalyzer
from apps.resume_checker.services.projects_analyzer import ResumeProjectsAnalyzer
from apps.resume_checker.services.recommendation_engine import ResumeRecommendationEngine
from apps.resume_checker.services.skills_analyzer import ResumeSkillsAnalyzer
from apps.resume_checker.services.structure_analyzer import ResumeStructureAnalyzer
from apps.resumes.models import Resume


class ResumeScoreService:

    WEIGHTS = {
        "structure_score": Decimal(
            "0.20"
        ),
        "skills_score": Decimal(
            "0.25"
        ),
        "experience_score": Decimal(
            "0.25"
        ),
        "projects_score": Decimal(
            "0.15"
        ),
        "keyword_score": Decimal(
            "0.15"
        ),
    }

    @staticmethod
    def get_resume(
        user
    ):
        return (
            Resume.objects.filter(
                user=user
            )
            .select_related(
                "analysis"
            )
            .prefetch_related(
                "skills__skill",
                "experiences",
                "educations",
                "projects",
            )
            .first()
        )

    @classmethod
    def analyze(
        cls,
        user
    ):
        resume = cls.get_resume(
            user
        )

        if not resume:
            return None

        structure = ResumeStructureAnalyzer.analyze(
            resume
        )
        skills = ResumeSkillsAnalyzer.analyze(
            resume
        )
        experience = ResumeExperienceAnalyzer.analyze(
            resume
        )
        projects = ResumeProjectsAnalyzer.analyze(
            resume
        )
        keywords = ResumeKeywordAnalyzer.analyze(
            resume
        )

        component_scores = {
            "structure_score": Decimal(
                str(
                    structure["score"]
                )
            ),
            "skills_score": Decimal(
                str(
                    skills["score"]
                )
            ),
            "experience_score": Decimal(
                str(
                    experience["score"]
                )
            ),
            "projects_score": Decimal(
                str(
                    projects["score"]
                )
            ),
            "keyword_score": Decimal(
                str(
                    keywords["score"]
                )
            ),
        }

        overall_score = sum(
            component_scores[name] * weight
            for name, weight in cls.WEIGHTS.items()
        ).quantize(
            Decimal(
                "0.01"
            )
        )

        recommendation_data = ResumeRecommendationEngine.combine(
            [
                structure,
                skills,
                experience,
                projects,
                keywords,
            ]
        )

        with transaction.atomic():
            score, _ = ResumeScore.objects.update_or_create(
                user=user,
                defaults={
                    **component_scores,
                    "overall_score": overall_score,
                    "strengths": recommendation_data[
                        "strengths"
                    ],
                    "weaknesses": recommendation_data[
                        "weaknesses"
                    ],
                    "recommendations": recommendation_data[
                        "recommendations"
                    ],
                },
            )

        score.matched_keywords = keywords.get(
            "matched_keywords",
            [],
        )
        score.missing_keywords = keywords.get(
            "missing_keywords",
            [],
        )

        return score

    @staticmethod
    def get_latest(
        user
    ):
        return ResumeScore.objects.filter(
            user=user
        ).first()

