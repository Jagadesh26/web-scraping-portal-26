from rest_framework import serializers

from apps.profiles.models import Profile


class ProfileSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        source="user.email",
        read_only=True
    )

    class Meta:

        model = Profile

        fields = (
            "id",
            "email",
            "full_name",
            "phone",
            "location",
            "current_role",
            "experience_years",
            "linkedin_url",
            "github_url",
            "portfolio_url",
        )