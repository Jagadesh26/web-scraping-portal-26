from rest_framework import serializers

from apps.profiles.models import JobRole


class JobRoleSerializer(serializers.ModelSerializer):

    class Meta:

        model = JobRole

        fields = (
            "id",
            "name",
        )