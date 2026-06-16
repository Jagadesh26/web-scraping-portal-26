LEVER_COMPANIES = [
    # --- Tier 1 Tech & Core DevTools ---
    "netlify",
    "postman",
    "circleci",
    "figma",
    "vercel",
    "docker",
    "digitalocean",
    "elastic",
    "gitlab",
    "snyk",
    "palantir",
    "cockroachlabs",
    "couchbase",
    "cloudera",
    "confluent",

    # --- FinTech & Modern Finance ---
    "plaid",
    "brex",
    "ramp",
    "gusto",
    "chime",
    "sofi",
    "affirm",
    "robinhood",
    "coinbase",
    "ripple",
    "kraken",
    "consensys",
    "blockfi",
    "wealthfront",
    "betterment",

    # --- AI, ML & Data Engineering ---
    "openai",
    "anthropic",
    "scale",
    "databricks",
    "dataiku",
    "fivetran",
    "airbyte",
    "dbtlabs",
    "huggingface",
    "weightsandbiases",
    "anyscale",
    "cohere",
    "assemblyai",
    "replicate",
    "pinecone",

    # --- SaaS, Productivity & Collaboration ---
    "canva",
    "miro",
    "loom",
    "clickup",
    "airtable",
    "zapier",
    "notion",
    "webflow",
    "framer",
    "gong",
    "chorus",
    "intercom",
    "hubspot",
    "buffer",
    "frontapp",

    # --- Security, Cloud & Infrastructure ---
    "auth0",
    "okta",
    "cloudflare",
    "fastly",
    "datadog",
    "grafana",
    "logrocket",
    "launchdarkly",
    "hashicorp",
    "pagerduty",
    "opsgenie",
    "splunk",
    "lacework",
    "wiz",
    "tanium",

    # --- Consumer Apps, EdTech & Media ---
    "spotify",
    "duolingo",
    "coursera",
    "udemy",
    "medium",
    "substack",
    "patreon",
    "discord",
    "twitch",
    "vimeo",
    "genius",
    "classpass",
    "masterclass",
    "quizlet",
    "codecademy",

    # --- Logistics, Operations & Hardware ---
    "flexport",
    "deliveroo",
    "instacart",
    "doordash",
    "getir",
    "bolt",
    "deliveryhero",
    "gopuff",
    "bird",
    "lime",
]


import requests

from apps.jobs.collectors.base import (
    BaseCollector,
)



from apps.jobs.services.normalization_service import (
    JobNormalizationService,
)


class LeverCollector(
    BaseCollector
):

    source_name = "Lever"

    base_url = "https://jobs.lever.co"

    def fetch_jobs(
        self
    ):

        all_jobs = []

        for company in LEVER_COMPANIES:

            try:

                url = (
                    f"https://api.lever.co/v0/postings/"
                    f"{company}?mode=json"
                )

                response = requests.get(
                    url,
                    timeout=30,
                )

                response.raise_for_status()

                jobs = response.json()

                for job in jobs:

                    job[
                        "_company_slug"
                    ] = company

                all_jobs.extend(
                    jobs
                )

            except Exception as e:

                print(
                    f"Lever {company} failed: {e}"
                )

        return all_jobs

    def normalize(
        self,
        raw_job
    ):

        return (
            JobNormalizationService
            .normalize_lever(
                raw_job
            )
        )