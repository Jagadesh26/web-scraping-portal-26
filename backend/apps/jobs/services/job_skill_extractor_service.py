from apps.jobs.models import (
    JobSkill
)

from apps.resumes.models import (
    Skill
)


class JobSkillExtractorService:

    @staticmethod
    def extract_skills(
        job
    ):

        text = (
            job.description or ""
        ).lower()

        skills = Skill.objects.all()

        created_count = 0

        for skill in skills:

            if (
                skill.name.lower()
                in text
            ):

                JobSkill.objects.get_or_create(
                    job=job,
                    skill=skill
                )

                created_count += 1

        return created_count