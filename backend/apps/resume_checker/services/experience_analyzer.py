from decimal import Decimal

from django.core.exceptions import ObjectDoesNotExist

from apps.resume_checker.services.base import AnalyzerBase


class ResumeExperienceAnalyzer(AnalyzerBase):

    @classmethod
    def analyze(
        cls,
        resume
    ):
        experiences = list(
            resume.experiences.all()
        )
        try:
            analysis = resume.analysis
        except ObjectDoesNotExist:
            analysis = None

        score = 0
        strengths = []
        weaknesses = []
        recommendations = []

        if len(
            experiences
        ) >= 2:
            score += 30
            strengths.append(
                "Multiple experience entries are available."
            )
        elif len(
            experiences
        ) == 1:
            score += 20
            strengths.append(
                "Experience section is present."
            )
        else:
            weaknesses.append(
                "Experience entries are missing."
            )
            recommendations.append(
                "Add work experience, internships, freelance work, or relevant training."
            )

        total_experience = Decimal(
            "0"
        )
        if analysis:
            total_experience = analysis.total_experience or Decimal(
                "0"
            )

        if total_experience >= 2:
            score += 25
            strengths.append(
                "Years of experience are clearly represented."
            )
        elif total_experience > 0:
            score += 15
        elif experiences:
            score += 8
            recommendations.append(
                "Mention dates or duration so ATS systems can read your experience."
            )

        strong_descriptions = 0
        measurable_descriptions = 0

        for experience in experiences:
            description = cls.normalize_text(
                experience.description
            )
            if len(
                description
            ) >= 80:
                strong_descriptions += 1
            if cls.has_number(
                description
            ):
                measurable_descriptions += 1

        if experiences and strong_descriptions == len(
            experiences
        ):
            score += 30
            strengths.append(
                "Experience descriptions are detailed."
            )
        elif strong_descriptions:
            score += 18
            recommendations.append(
                "Expand shorter experience descriptions with responsibilities and impact."
            )
        elif experiences:
            score += 6
            weaknesses.append(
                "Experience descriptions are too short."
            )
            recommendations.append(
                "Use bullet points with action verbs, tools used, and outcomes."
            )

        if measurable_descriptions:
            score += 15
            strengths.append(
                "Measurable achievements are included."
            )
        elif experiences:
            weaknesses.append(
                "Measurable achievements are missing."
            )
            recommendations.append(
                "Add metrics such as percentages, time saved, revenue, users, or performance gains."
            )

        return {
            "score": cls.clamp_score(
                score
            ),
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": recommendations,
        }
