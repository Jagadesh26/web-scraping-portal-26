from django.db.models import Avg
from django.db.models import Max
from django.db.models import Min

from apps.jobs.models import Job, JobMatch



class ATSDashboardService:

    @staticmethod
    def get_dashboard(
        user
    ):

        matches = (
            JobMatch.objects.filter(
                user=user
            )
        )

        return {

            "total_jobs":
                Job.objects.filter(
                    is_active=True
                ).count(),

            "recommended_jobs":
                matches.count(),

            "average_match_score":
                round(
                    matches.aggregate(
                        Avg("final_score")
                    )[
                        "final_score__avg"
                    ] or 0,
                    2
                ),

            "highest_match_score":
                round(
                    matches.aggregate(
                        Max("final_score")
                    )[
                        "final_score__max"
                    ] or 0,
                    2
                ),

            "lowest_match_score":
                round(
                    matches.aggregate(
                        Min("final_score")
                    )[
                        "final_score__min"
                    ] or 0,
                    2
                ),
        }