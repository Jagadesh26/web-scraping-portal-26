from apps.jobs.models import (
    JobSkill,
    Job
)

from apps.resumes.models import (
    ResumeSkill
)

from apps.jobs.models import (
    Job,
    JobMatch
)


class ATSMatchingService:

    @staticmethod
    def calculate_score(
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

            return None

        matched_skills = list(
            resume_skills.intersection(
                job_skills
            )
        )

        missing_skills = list(
            job_skills -
            resume_skills
        )

        score = (
            len(matched_skills)
            /
            len(job_skills)
        ) * 100

        job_match, _ = (
            JobMatch.objects.update_or_create(
                user=user,
                job=job,
                defaults={
                    "score": score,
                    "matched_skills":
                        matched_skills,
                    "missing_skills":
                        missing_skills,
                }
            )
        )

        return job_match