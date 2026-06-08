from rest_framework import serializers

from apps.profiles.models import (
    UserJobPreference,
    JobRole
)


class UserJobPreferenceSerializer(
    serializers.ModelSerializer
):

    job_role_name = serializers.CharField(
        source="job_role.name",
        read_only=True
    )

    class Meta:

        model = UserJobPreference

        fields = (
            "id",
            "job_role",
            "job_role_name",
            "is_primary",
        )

    def validate_job_role(self, value):

        if not JobRole.objects.filter(
            id=value.id
        ).exists():
            raise serializers.ValidationError(
                "Invalid job role."
            )

        return value