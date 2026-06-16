from abc import ABC
from abc import abstractmethod


class BaseCollector(
    ABC
):

    source_name = ""

    base_url = ""

    @abstractmethod
    def fetch_jobs(
        self
    ):
        """
        Return raw jobs from source.
        """
        pass

    @abstractmethod
    def normalize(
        self,
        raw_job,
    ):
        """
        Convert raw job
        into unified format.
        """
        pass