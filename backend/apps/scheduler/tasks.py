from celery import shared_task

from apps.jobs.services.collection_service import (
    JobCollectionService
)

from apps.jobs.services.stale_job_service import (
    StaleJobService
)

from apps.jobs.services.job_cleanup_service import (
    JobCleanupService
)



@shared_task
def collect_jobs_task():

    return (
        JobCollectionService
        .collect_all()
    )



@shared_task
def deactivate_stale_jobs_task():

    return (
        StaleJobService
        .deactivate_stale_jobs()
    )



@shared_task
def cleanup_jobs_task():

    return (
        JobCleanupService
        .cleanup()
    )