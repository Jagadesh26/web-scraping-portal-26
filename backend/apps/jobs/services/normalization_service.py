class JobNormalizationService:

    @staticmethod
    def normalize_remoteok(
        raw_job
    ):

        return {

            "external_job_id":
                str(
                    raw_job.get("id")
                ),

            "title":
                raw_job.get(
                    "position"
                ),

            "company_name":
                raw_job.get(
                    "company"
                ),

            "location":
                raw_job.get(
                    "location",
                    ""
                ),

            "description":
                raw_job.get(
                    "description",
                    ""
                ),

            "apply_url":
                raw_job.get(
                    "url"
                ),

            "posted_at":
                raw_job.get(
                    "date"
                ),

            "raw_payload":
                raw_job,

            "skills":
                raw_job.get(
                    "tags",
                    []
                ),
        }