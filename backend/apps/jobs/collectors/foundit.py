import requests

from apps.jobs.models import SearchKeyword


class FounditCollector:

    BASE_URL = (
        "https://www.foundit.in/home/api/searchResultsPage"
    )

    LIMIT = 20

    def fetch_jobs(self):

        jobs = []

        keywords = (
            SearchKeyword.objects.filter(
                is_active=True
            )
        )

        for keyword in keywords:

            jobs.extend(
                self.fetch_keyword_jobs(
                    keyword.keyword
                )
            )

        return jobs

    def fetch_keyword_jobs(
        self,
        keyword,
    ):

        results = []

        start = 0

        while True:

            params = {

                "start": start,

                "limit": self.LIMIT,

                "query": keyword,

                "queryDerived": "true",

                "countries": "India",

                "variantName": "DEFAULT",
            }

            response = requests.get(
                self.BASE_URL,
                params=params,
                timeout=30,
            )

            response.raise_for_status()

            payload = response.json()

            jobs = payload.get(
                "data",
                []
            )

            if not jobs:

                break

            results.extend(
                jobs
            )

            start += self.LIMIT

            if start >= 100:
                break

        return results