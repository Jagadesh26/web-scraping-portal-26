from apps.resumes.models import (
    Skill,
    ResumeSkill
)


class SkillExtractorService:

    @staticmethod
    def extract_skills(
        resume,
        raw_text
    ):

        if not raw_text:
            return []

        extracted_skills = []

        text = raw_text.lower()

        skills = Skill.objects.all()

        for skill in skills:

            if skill.name.lower() in text:

                ResumeSkill.objects.get_or_create(
                    resume=resume,
                    skill=skill,
                    defaults={
                        "confidence_score": 100
                    }
                )

                extracted_skills.append(
                    skill.name
                )

        return extracted_skills
