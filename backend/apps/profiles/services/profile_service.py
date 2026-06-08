from apps.profiles.models import Profile


class ProfileService:

    @staticmethod
    def get_profile(user):

        return Profile.objects.get(
            user=user
        )

    @staticmethod
    def update_profile(
        profile,
        validated_data
    ):

        for key, value in validated_data.items():
            setattr(
                profile,
                key,
                value
            )

        profile.save()

        return profile