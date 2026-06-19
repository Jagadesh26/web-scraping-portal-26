import logging

from apps.ats.services.ats_matching_service import ATSMatchingService
from apps.jobs.models import Job, JobMatch

logger = logging.getLogger(__name__)


class ATSAnalysisService:

    @classmethod
    def process_resume_jobs(
        cls,
        resume
    ):
        jobs = Job.objects.filter(
            is_active=True
        ).prefetch_related(
            "job_skills__skill"
        )
        processed = 0

        for job in jobs:
            try:
                match = ATSMatchingService.calculate(
                    user=resume.user,
                    job=job
                )

                if match:
                    processed += 1

            except Exception:
                logger.exception(
                    "ATS analysis failed for resume %s and job %s",
                    resume.id,
                    job.id,
                )

        return {
            "total_jobs": jobs.count(),
            "processed_matches": processed,
            "stored_matches": JobMatch.objects.filter(
                user=resume.user
            ).count(),
        }
