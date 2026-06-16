from apps.jobs.models import (
    Job,
    JobMatch
)

from apps.ats.services.ats_matching_service import (
    ATSMatchingService
)




class RecommendationService:

    @staticmethod
    def generate(
        user
    ):

        jobs = Job.objects.filter(
            is_active=True
        )

        for job in jobs:

            ATSMatchingService.calculate(
                user=user,
                job=job
            )

        return (
            JobMatch.objects.filter(
                user=user
            )
            .order_by(
                "-final_score"
            )
        )