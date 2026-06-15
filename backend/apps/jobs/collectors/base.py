from abc import ABC, abstractmethod


class BaseCollector(ABC):

    @abstractmethod
    def fetch_jobs(self):
        pass

    @abstractmethod
    def normalize_job(
        self,
        raw_job
    ):
        pass