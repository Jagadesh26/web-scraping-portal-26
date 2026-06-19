from apps.jobs.models import (
    JobSkill
)

from apps.resumes.models import (
    Skill
)
from apps.resumes.services.skill_extractor_service import (
    SkillExtractorService
)


class JobSkillExtractorService:

    @staticmethod
    def extract_skills(
        job
    ):

        text = (
            job.description or ""
        ).lower()

        created_count = 0

        extracted_skills = SkillExtractorService.extract_skills_from_text(
            text
        )

        catalog_categories = dict(
            SkillExtractorService.get_catalog_items()
        )

        for skill_name in extracted_skills:

            skill, _ = Skill.objects.get_or_create(
                name=skill_name,
                defaults={
                    "category": catalog_categories.get(
                        skill_name,
                        ""
                    )
                }
            )

            _, created = JobSkill.objects.get_or_create(
                job=job,
                skill=skill
            )

            if created:
                created_count += 1

        for skill in Skill.objects.all():

            if skill.name.lower() in text:

                _, created = JobSkill.objects.get_or_create(
                    job=job,
                    skill=skill
                )

                if created:
                    created_count += 1

        return created_count
