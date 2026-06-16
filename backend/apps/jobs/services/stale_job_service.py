from datetime import timedelta

from django.utils import timezone

from apps.jobs.models import Job


class StaleJobService:

    @staticmethod
    def deactivate_stale_jobs():

        cutoff_date = (
            timezone.now()
            -
            timedelta(days=14)
        )

        updated_count = (
            Job.objects.filter(
                is_active=True,
                last_seen_at__lt=cutoff_date
            )
            .update(
                is_active=False
            )
        )

        return updated_count