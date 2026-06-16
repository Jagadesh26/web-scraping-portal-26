

from apps.ats.services.skill_matching_service import (
    SkillMatchingService
)

from apps.ats.services.experience_matching_service import (
    ExperienceMatchingService
)

from apps.ats.services.preference_matching_service import (
    PreferenceMatchingService
)
from apps.jobs.models import JobMatch


class ATSMatchingService:

    @staticmethod
    def calculate(
        user,
        job
    ):

        skill_result = (
            SkillMatchingService.calculate(
                user=user,
                job=job
            )
        )

        skill_score = (
            skill_result["score"]
        )

        experience_score = (
            ExperienceMatchingService.calculate(
                user=user,
                job=job
            )
        )

        preference_score = (
            PreferenceMatchingService.calculate(
                user=user,
                job=job
            )
        )

        final_score = round(

            (
                skill_score * 0.70
            )
            +
            (
                experience_score * 0.20
            )
            +
            (
                preference_score * 0.10
            ),

            2

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
                        preference_score,

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
                }
            )
        )

        return job_match