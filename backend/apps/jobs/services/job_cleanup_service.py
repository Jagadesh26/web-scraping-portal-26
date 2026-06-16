from datetime import timedelta

from django.utils import timezone

from apps.jobs.models import Job


class JobCleanupService:

    @staticmethod
    def cleanup():

        cutoff_date = (
            timezone.now()
            -
            timedelta(days=30)
        )

        deleted_count, _ = (
            Job.objects.filter(
                is_active=False,
                last_seen_at__lt=cutoff_date
            )
            .delete()
        )

        return deleted_count