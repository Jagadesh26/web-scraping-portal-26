from apps.jobs.models import Job
from apps.jobs.services.ats_matching_service import ATSMatchingService




class RecommendationService:

    @staticmethod
    def generate(
        user
    ):

        jobs = Job.objects.filter(
            is_active=True
        )

        matches = []

        for job in jobs:

            result = (
                ATSMatchingService
                .calculate_score(
                    user,
                    job
                )
            )

            if result:

                matches.append(
                    result
                )

        return matches