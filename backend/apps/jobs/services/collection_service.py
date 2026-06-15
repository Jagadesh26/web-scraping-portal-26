from django.utils import timezone

from apps.jobs.models import (
    Job,
    JobSource,
)

from apps.jobs.services.normalization_service import (
    JobNormalizationService
)

from apps.jobs.services.deduplication_service import (
    JobDeduplicationService
)


class JobCollectionService:

    @staticmethod
    def collect_remoteok(
        collector
    ):

        source, _ = (
            JobSource.objects.get_or_create(
                name="RemoteOK",
                defaults={
                    "base_url":
                    "https://remoteok.com"
                }
            )
        )

        jobs = (
            collector.fetch_jobs()
        )

        count = 0

        for raw_job in jobs:

            normalized = (
                JobNormalizationService
                .normalize_remoteok(
                    raw_job
                )
            )

            existing_job = (
                JobDeduplicationService
                .get_existing_job(
                    source,
                    normalized[
                        "external_job_id"
                    ]
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

            job=Job.objects.create(
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
                location=normalized[
                    "location"
                ],
                description=normalized[
                    "description"
                ],
                apply_url=normalized[
                    "apply_url"
                ],
                raw_payload=normalized[
                    "raw_payload"
                ],
                posted_at=normalized[
                    "posted_at"
                ],
                last_seen_at=timezone.now(),
                is_active=True,
            )

            count += 1


        from apps.jobs.services.job_skill_extractor_service import (
            JobSkillExtractorService
        )
        JobSkillExtractorService.extract_skills(
            job
        )

        return count