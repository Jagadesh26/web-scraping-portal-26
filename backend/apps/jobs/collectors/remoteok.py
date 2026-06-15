import requests

from .base import BaseCollector


class RemoteOKCollector(
    BaseCollector
):

    URL = (
        "https://remoteok.com/api"
    )

    def fetch_jobs(self):

        response = requests.get(
            self.URL,
            headers={
                "User-Agent":
                "Mozilla/5.0"
            },
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        return data[1:]
    
    def normalize_job(self, raw_job):
        return super().normalize_job(raw_job)