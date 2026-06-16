from django.utils import timezone

from apps.jobs.collectors.greenhouse import GreenhouseCollector
from apps.jobs.collectors.lever import LeverCollector
from apps.jobs.collectors.workday import WorkdayCollector
from apps.jobs.models import (
    Job,
    JobSource,
)

from apps.jobs.services.deduplication_service import (
    JobDeduplicationService,
)

from apps.jobs.services.job_skill_extractor_service import (
    JobSkillExtractorService,
)

from apps.jobs.collectors.remoteok import (
    RemoteOKCollector,
)

from apps.jobs.collectors.wellfound import (
    WellfoundCollector,
)


COLLECTORS = [

    RemoteOKCollector,

    WellfoundCollector,

    LeverCollector,

    GreenhouseCollector,

    WorkdayCollector,

]


class JobCollectionService:

    @staticmethod
    def collect(
        collector
    ):

        source, _ = (
            JobSource.objects.get_or_create(
                name=collector.source_name,
                defaults={
                    "base_url":
                    collector.base_url,
                },
            )
        )

        jobs = (
            collector.fetch_jobs()
        )

        count = 0

        for raw_job in jobs:

            normalized = (
                collector.normalize(
                    raw_job
                )
            )

            existing_job = (
                JobDeduplicationService
                .get_existing_job(
                    source,
                    normalized[
                        "external_job_id"
                    ],
                )
            )

            if existing_job:

                existing_job.last_seen_at = (
                    timezone.now()
                )

                existing_job.is_active = True

                existing_job.save(
                    update_fields=[
                        "last_seen_at",
                        "is_active",
                    ]
                )

                continue

            job = Job.objects.create(

                job_source=source,

                external_job_id=normalized[
                    "external_job_id"
                ],

                title=normalized[
                    "title"
                ],

                company_name=normalized[
                    "company_name"
                ],

                location=normalized.get(
                    "location",
                    "",
                ),

                employment_type=normalized.get(
                    "employment_type",
                    "",
                ),

                experience_min=normalized.get(
                    "experience_min"
                ),

                experience_max=normalized.get(
                    "experience_max"
                ),

                salary_min=normalized.get(
                    "salary_min"
                ),

                salary_max=normalized.get(
                    "salary_max"
                ),

                currency=normalized.get(
                    "currency",
                    "",
                ),

                description=normalized.get(
                    "description",
                    "",
                ),

                apply_url=normalized[
                    "apply_url"
                ],

                posted_at=normalized.get(
                    "posted_at"
                ),

                raw_payload=normalized.get(
                    "raw_payload",
                    {},
                ),

                last_seen_at=timezone.now(),

                is_active=True,
            )

            JobSkillExtractorService.extract_skills(
                job
            )

            count += 1

        source.last_sync_at = (
            timezone.now()
        )

        source.save(
            update_fields=[
                "last_sync_at"
            ]
        )

        return count

    @staticmethod
    def collect_all():

        total = 0

        for collector_class in COLLECTORS:

            try:

                collector = (
                    collector_class()
                )

                total += (
                    JobCollectionService.collect(
                        collector
                    )
                )

            except Exception as e:

                print(
                    f"{collector_class.__name__} failed: {e}"
                )

        return total