from rest_framework import serializers

from apps.resumes.models import Resume


class ResumeSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = Resume

        fields = (
            "id",
            "file_name",
            "file_url",
            "file_size",
            "file_type",
            "status",
            "uploaded_at",
        )