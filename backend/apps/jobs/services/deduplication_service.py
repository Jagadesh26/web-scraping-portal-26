from apps.jobs.models import Job


class JobDeduplicationService:

    @staticmethod
    def get_existing_job(
        source,
        external_job_id
    ):

        return Job.objects.filter(
            job_source=source,
            external_job_id=external_job_id
        ).first()