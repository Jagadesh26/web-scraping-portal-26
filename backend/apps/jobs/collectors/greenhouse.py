
import requests

from apps.jobs.collectors.base import (
    BaseCollector,
)


from apps.jobs.services.normalization_service import (
    JobNormalizationService,
)


GREENHOUSE_COMPANIES = [
    # --- Tier 1 Tech / Anchors ---
    "stripe",
    "notion",
    "discord",
    "github",
    "reddit",
    "airbnb",
    "coinbase",
    "robinhood",
    "figma",
    "hashicorp",
    "elastic",
    "twitch",
    "squarespace",
    "vimeo",
    "box",
    
    # --- High-Growth Tech & Platforms ---
    "pinterest",
    "doordash",
    "instacart",
    "lyft",
    "snapchat",
    "brex",
    "ramp",
    "plaid",
    "gusto",
    "chime",
    "revolut",
    "wise",
    "toast",
    "klarna",
    "checkout",

    # --- AI & Data Infrastructure ---
    "openai",
    "anthropic",
    "scaleai",
    "huggingface",
    "databricks",
    "snowflake",
    "confluent",
    "mongodb",
    "cockroachlabs",
    "clickhouse",
    "dbtlabs",
    "fivetran",
    "airbyte",
    "grafana",
    "datadog",

    # --- Developer Tools & Security ---
    "gitlab",
    "snyk",
    "auth0",
    "okta",
    "vercel",
    "netlify",
    "supabase",
    "planetscale",
    "docker",
    "postman",
    "pagerduty",
    "fastly",
    "cloudflare",
    "digitalocean",
    "temporal",

    # --- Enterprise SaaS & Productivity ---
    "zoom",
    "miro",
    "canva",
    "loom",
    "asana",
    "monday",
    "clickup",
    "airtable",
    "zapier",
    "intercom",
    "hubspot",
    "freshworks",
    "gong",
    "amplitude",
    "mixpanel",

    # --- Consumer, Web3 & Digital Giants ---
    "spotify",
    "duolingo",
    "coursera",
    "udemy",
    "medium",
    "substack",
    "patreon",
    "deliveroo",
    "canopygrowth",
    "kraken",
    "gemini",
    "chainlink",
    "ledger",
    "polygon",
    "opensea",

    # --- Modern Operations & Hardware ---
    "flexport",
    "convoy",
    "anduril",
    "spacex",
    "rivian",
    "lucidmotors",
    "toast",
    "doordash",
    "bolt",
    "deliveryhero",
]





class GreenhouseCollector(
    BaseCollector
):

    source_name = "Greenhouse"

    base_url = "https://boards.greenhouse.io"

    def fetch_jobs(
        self
    ):

        all_jobs = []

        for company in GREENHOUSE_COMPANIES:

            try:

                url = (
                    f"https://boards-api.greenhouse.io/v1/boards/"
                    f"{company}/jobs"
                )

                response = requests.get(
                    url,
                    timeout=30,
                )

                response.raise_for_status()

                data = response.json()

                jobs = data.get(
                    "jobs",
                    []
                )

                for job in jobs:

                    job[
                        "_company_slug"
                    ] = company

                all_jobs.extend(
                    jobs
                )

            except Exception as e:

                print(
                    f"Greenhouse {company} failed: {e}"
                )

        return all_jobs

    def normalize(
        self,
        raw_job
    ):

        return (
            JobNormalizationService
            .normalize_greenhouse(
                raw_job
            )
        )