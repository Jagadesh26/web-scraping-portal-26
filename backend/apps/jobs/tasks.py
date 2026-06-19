from celery import shared_task

import asyncio

from apps.jobs.collectors.foundit import (
    FounditCollector,
)


@shared_task
def collect_foundit_jobs():

    collector = (
        FounditCollector()
    )

    asyncio.run(
        collector.collect()
    )