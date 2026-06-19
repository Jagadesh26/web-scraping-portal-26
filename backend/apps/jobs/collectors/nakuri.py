import requests
from urllib.parse import quote

from apps.jobs.models import SearchKeyword


class NaukriCollector:

    BASE_URL = (
        "https://www.naukri.com/jobapi/v3/search"
    )

    LIMIT = 20
    MAX_PAGES = 5

    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/137.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json",
        "Referer": "https://www.naukri.com/",
    }

    def fetch_jobs(self):

        all_jobs = []

        keywords = SearchKeyword.objects.filter(
            is_active=True
        )

        for keyword_obj in keywords:

            keyword = keyword_obj.keyword

            jobs = self.fetch_keyword_jobs(
                keyword
            )

            all_jobs.extend(
                jobs
            )

        return all_jobs

    def fetch_keyword_jobs(
        self,
        keyword,
    ):

        jobs = []

        seo_key = (
            keyword.lower()
            .replace(" ", "-")
        )

        for page in range(
            1,
            self.MAX_PAGES + 1
        ):

            params = {

                "noOfResults": self.LIMIT,

                "urlType":
                    "search_by_keyword",

                "searchType":
                    "adv",

                "keyword":
                    keyword,

                "pageNo":
                    page,

                "k":
                    keyword,

                "seoKey":
                    seo_key,

                "src":
                    "jobsearchDesk",

                "latLong":
                    "",
            }

            try:

                response = requests.get(
                    self.BASE_URL,
                    params=params,
                    headers=self.HEADERS,
                    timeout=30,
                )

                response.raise_for_status()

                payload = response.json()

                page_jobs = payload.get(
                    "jobDetails",
                    []
                )

                if not page_jobs:
                    break

                jobs.extend(
                    page_jobs
                )

            except Exception as e:

                print(
                    f"Naukri Error "
                    f"{keyword} "
                    f"Page {page}: "
                    f"{str(e)}"
                )

                continue

        return jobs