from apps.resume_checker.services.base import AnalyzerBase
from apps.resume_checker.services.constants import MODERN_SKILLS, WEAK_SKILLS


class ResumeSkillsAnalyzer(AnalyzerBase):

    @classmethod
    def analyze(
        cls,
        resume
    ):
        skills = list(
            resume.skills.select_related(
                "skill"
            )
        )
        skill_names = [
            item.skill.name.strip()
            for item in skills
            if item.skill.name
        ]
        normalized = {
            item.lower()
            for item in skill_names
        }

        score = 0
        strengths = []
        weaknesses = []
        recommendations = []

        skill_count = len(
            normalized
        )

        if skill_count >= 8:
            score += 40
            strengths.append(
                "Strong number of skills detected."
            )
        elif skill_count >= 4:
            score += 25
            strengths.append(
                "Core skills are present."
            )
        elif skill_count > 0:
            score += 10
            weaknesses.append(
                "Skills list is too short."
            )
            recommendations.append(
                "Add more role-relevant technical skills."
            )
        else:
            weaknesses.append(
                "No skills detected."
            )
            recommendations.append(
                "Add a clear skills section with technical keywords."
            )

        weak_matches = normalized.intersection(
            WEAK_SKILLS
        )
        technical_count = skill_count - len(
            weak_matches
        )

        if technical_count >= 5:
            score += 35
            strengths.append(
                "Good technical skill coverage."
            )
        elif technical_count >= 2:
            score += 20
        elif skill_count:
            score += 5
            weaknesses.append(
                "Skills are not technical enough for ATS matching."
            )
            recommendations.append(
                "Replace generic skills with specific tools, languages, and frameworks."
            )

        modern_matches = normalized.intersection(
            MODERN_SKILLS
        )

        if len(
            modern_matches
        ) >= 3:
            score += 25
            strengths.append(
                "Modern tools and technologies are included."
            )
        elif modern_matches:
            score += 12
            recommendations.append(
                "Add more modern technologies such as Docker, AWS, Redis, or CI/CD."
            )
        else:
            weaknesses.append(
                "Modern technologies are missing."
            )
            recommendations.append(
                "Add modern tools such as Docker, AWS, Redis, or CI/CD if you have used them."
            )

        return {
            "score": cls.clamp_score(
                score
            ),
            "strengths": strengths,
            "weaknesses": weaknesses,
            "recommendations": recommendations,
        }

