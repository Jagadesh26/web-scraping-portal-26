import requests

from apps.jobs.collectors.base import (
    BaseCollector,
)

from apps.jobs.services.normalization_service import (
    JobNormalizationService,
)


class RemoteOKCollector(
    BaseCollector
):

    source_name = "RemoteOK"

    base_url = "https://remoteok.com"

    API_URL = (
        "https://remoteok.com/api"
    )

    def fetch_jobs(
        self
    ):

        response = requests.get(
            self.API_URL,
            headers={
                "User-Agent":
                (
                    "Mozilla/5.0 "
                    "(Windows NT 10.0; Win64; x64)"
                )
            },
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        if not data:
            return []

        # First item contains metadata
        return data[1:]

    def normalize(
        self,
        raw_job,
    ):

        return (
            JobNormalizationService
            .normalize_remoteok(
                raw_job
            )
        )