


from apps.profiles.models.job_preference import UserJobPreference


class PreferenceMatchingService:

    @staticmethod
    def calculate(
        user,
        job
    ):

        preferences = (
            UserJobPreference.objects.filter(
                user=user
            )
        )

        if not preferences.exists():

            return 0

        job_title = (
            job.title.lower()
        )

        for preference in preferences:

            role_name = (
                preference.job_role.name.lower()
            )

            if (
                role_name in job_title
                or
                job_title in role_name
            ):

                return 100

        return 0