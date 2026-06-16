from django.core.exceptions import ObjectDoesNotExist

from apps.resume_checker.services.base import AnalyzerBase
from apps.resume_checker.services.constants import MARKET_SKILLS


class ResumeKeywordAnalyzer(AnalyzerBase):

    @classmethod
    def analyze(
        cls,
        resume
    ):
        skills = {
            item.skill.name.lower()
            for item in resume.skills.select_related(
                "skill"
            )
            if item.skill.name
        }
        project_text = " ".join(
            f"{project.description} {project.technologies}"
            for project in resume.projects.all()
        )
        experience_text = " ".join(
            experience.description
            for experience in resume.experiences.all()
        )
        try:
            analysis = resume.analysis
        except ObjectDoesNotExist:
            analysis = None
        raw_text = analysis.raw_text if analysis else ""

        resume_text = " ".join(
            [
                " ".join(
                    skills
                ),
                project_text,
                experience_text,
                raw_text,
            ]
        ).lower()

        matched_keywords = sorted(
            keyword
            for keyword in MARKET_SKILLS
            if keyword in skills or keyword in resume_text
        )
        missing_keywords = sorted(
            MARKET_SKILLS.difference(
                matched_keywords
            )
        )

        score = (
            len(
                matched_keywords
            )
            / len(
                MARKET_SKILLS
            )
        ) * 100

        strengths = []
        weaknesses = []
        recommendations = []

        if score >= 70:
            strengths.append(
                "Strong market keyword coverage."
            )
        elif score >= 40:
            strengths.append(
                "Some important ATS keywords are present."
            )
            weaknesses.append(
                "Several market keywords are missing."
            )
        else:
            weaknesses.append(
                "Market keyword coverage is low."
            )

        for keyword in missing_keywords[:5]:
            recommendations.append(
                f"Add {keyword} if it matches your real experience."
            )

        return {
            "score": cls.clamp_score(
                score
            ),
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": recommendations,
            "matched_keywords": matched_keywords,
            "missing_keywords": missing_keywords,
        }
