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
                    "position",
                    ""
                ),

            "company_name":
                raw_job.get(
                    "company",
                    ""
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
                    "url",
                    ""
                ),

            "posted_at":
                raw_job.get(
                    "date"
                ),

            "employment_type":
                "REMOTE",

            "experience_min":
                None,

            "experience_max":
                None,

            "salary_min":
                None,

            "salary_max":
                None,

            "currency":
                "",

            "raw_payload":
                raw_job,

            "skills":
                raw_job.get(
                    "tags",
                    []
                ),
        }
    

    @staticmethod
    def normalize_greenhouse(
        raw_job
    ):

        location = ""

        if raw_job.get(
            "location"
        ):

            location = (
                raw_job["location"]
                .get(
                    "name",
                    ""
                )
            )

        return {

            "external_job_id":
                str(
                    raw_job.get(
                        "id"
                    )
                ),

            "title":
                raw_job.get(
                    "title"
                ),

            "company_name":
                raw_job.get(
                    "_company_slug",
                    ""
                ),

            "location":
                location,

            "description":
                "",

            "apply_url":
                raw_job.get(
                    "absolute_url"
                ),

            "posted_at":
                None,

            "employment_type":
                "",

            "experience_min":
                None,

            "experience_max":
                None,

            "salary_min":
                None,

            "salary_max":
                None,

            "currency":
                "",

            "raw_payload":
                raw_job,

            "skills":
                [],
        }
    

    @staticmethod
    def normalize_lever(
        raw_job
    ):

        categories = (
            raw_job.get(
                "categories",
                {}
            )
        )

        return {

            "external_job_id":
                str(
                    raw_job.get(
                        "id"
                    )
                ),

            "title":
                raw_job.get(
                    "text",
                    ""
                ),

            "company_name":
                raw_job.get(
                    "_company_slug",
                    ""
                ),

            "location":
                categories.get(
                    "location",
                    ""
                ),

            "description":
                raw_job.get(
                    "descriptionPlain",
                    ""
                ),

            "apply_url":
                raw_job.get(
                    "hostedUrl",
                    ""
                ),

            "posted_at":
                None,

            "employment_type":
                categories.get(
                    "commitment",
                    ""
                ),

            "experience_min":
                None,

            "experience_max":
                None,

            "salary_min":
                None,

            "salary_max":
                None,

            "currency":
                "",

            "raw_payload":
                raw_job,

            "skills":
                [],
        }
    


    @staticmethod
    def normalize_workday(
        raw_job
    ):

        return {

            "external_job_id":
                str(
                    raw_job.get(
                        "externalPath",
                        ""
                    )
                ),

            "title":
                raw_job.get(
                    "title",
                    ""
                ),

            "company_name":
                raw_job.get(
                    "_company_name",
                    ""
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
                    "apply_url",
                    ""
                ),

            "posted_at":
                None,

            "employment_type":
                "",

            "experience_min":
                None,

            "experience_max":
                None,

            "salary_min":
                None,

            "salary_max":
                None,

            "currency":
                "",

            "raw_payload":
                raw_job,

            "skills":
                [],
        }
    

    @staticmethod
    def normalize_foundit(
        raw_job
    ):

        location = ""

        if raw_job.get(
            "locations"
        ):

            location = (
                raw_job["locations"][0]
                .get(
                    "city",
                    ""
                )
            )

        return {

            "external_job_id":
                str(
                    raw_job.get(
                        "id"
                    )
                ),

            "title":
                raw_job.get(
                    "title",
                    ""
                ),

            "company_name":
                raw_job.get(
                    "company",
                    {}
                ).get(
                    "name",
                    ""
                ),

            "location":
                location,

            "description":
                raw_job.get(
                    "description",
                    ""
                ),

            "apply_url":
                "",

            "posted_at":
                raw_job.get(
                    "postedAt"
                ),

            "raw_payload":
                raw_job,

            "skills":
                [
                    skill["text"]
                    for skill in raw_job.get(
                        "itSkills",
                        []
                    )
                ],
        }


    @staticmethod
    def normalize_naukri(
        raw_job
    ):

        location = ""

        placeholders = raw_job.get(
            "placeholders",
            []
        )

        for item in placeholders:

            if item.get(
                "type"
            ) == "location":

                location = item.get(
                    "label",
                    ""
                )

                break

        return {

            "external_job_id":
                str(
                    raw_job.get(
                        "jobId"
                    )
                ),

            "title":
                raw_job.get(
                    "title",
                    ""
                ),

            "company_name":
                raw_job.get(
                    "companyName",
                    ""
                ),

            "location":
                location,

            "description":
                raw_job.get(
                    "jobDescription",
                    ""
                ),

            "apply_url":
                raw_job.get(
                    "applyRedirectUrl",
                    ""
                ),

            "posted_at":
                raw_job.get(
                    "createdDate"
                ),

            "raw_payload":
                raw_job,
        }

