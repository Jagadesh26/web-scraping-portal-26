from apps.jobs.collectors.base import BaseCollector


class WellfoundCollector(
    BaseCollector
):

    source_name = "Wellfound"

    base_url = "https://wellfound.com"

    def fetch_jobs(self):
        pass

    def normalize(self, raw_job):
        pass