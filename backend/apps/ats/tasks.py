from celery import shared_task

from apps.ats.services.analysis_service import ATSAnalysisService
from apps.resumes.models import Resume


@shared_task
def process_resume_jobs_task(
    resume_id
):
    resume = Resume.objects.filter(
        id=resume_id
    ).select_related(
        "user"
    ).first()

    if not resume:
        return {
            "total_jobs": 0,
            "processed_matches": 0,
            "stored_matches": 0,
        }

    return ATSAnalysisService.process_resume_jobs(
        resume
    )
