from abc import ABC
from abc import abstractmethod

from apps.jobs.collectors.base import (
    BaseCollector,
)


class PlaywrightCollector(
    BaseCollector,
    ABC,
):

    MAX_PAGES = 3

    @abstractmethod
    async def fetch_jobs(
        self
    ):
        pass

    @abstractmethod
    def normalize(
        self,
        raw_job,
    ):
        pass