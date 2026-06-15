from apps.jobs.models import (
    JobSkill
)

from apps.resumes.models import (
    ResumeSkill
)


class SkillMatchingService:

    @staticmethod
    def calculate(
        user,
        job
    ):

        resume_skills = set(

            ResumeSkill.objects.filter(
                resume__user=user
            ).values_list(
                "skill__name",
                flat=True
            )

        )

        job_skills = set(

            JobSkill.objects.filter(
                job=job
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
            }

        matched_skills = list(

            resume_skills.intersection(
                job_skills
            )

        )

        missing_skills = list(

            job_skills -
            resume_skills

        )

        score = round(

            (
                len(matched_skills)
                /
                len(job_skills)
            ) * 100,

            2

        )

        return {

            "score": score,

            "matched_skills":
                matched_skills,

            "missing_skills":
                missing_skills,
        }