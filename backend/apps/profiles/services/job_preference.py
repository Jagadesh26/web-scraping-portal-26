from apps.profiles.models import (
    UserJobPreference
)


class JobPreferenceService:

    @staticmethod
    def create_preference(
        user,
        job_role,
        is_primary=False
    ):

        if is_primary:

            UserJobPreference.objects.filter(
                user=user
            ).update(
                is_primary=False
            )

        preference = UserJobPreference.objects.create(
            user=user,
            job_role=job_role,
            is_primary=is_primary
        )

        return preference

    @staticmethod
    def list_preferences(user):

        return UserJobPreference.objects.filter(user=user).select_related("job_role")

    @staticmethod
    def delete_preference(preference):

        preference.delete()