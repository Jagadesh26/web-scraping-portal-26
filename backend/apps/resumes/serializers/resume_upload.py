from rest_framework import serializers
from django.conf import settings


class ResumeUploadSerializer(serializers.Serializer):

    resume = serializers.FileField()

    def validate_resume(self, file):

        extension = file.name.split(".")[-1].lower()

        allowed_extensions = (
            settings.ALLOWED_RESUME_EXTENSIONS
        )

        if extension not in allowed_extensions:
            raise serializers.ValidationError(
                "Only PDF and DOCX files are allowed."
            )

        max_size = (
            settings.MAX_RESUME_SIZE_MB
            * 1024
            * 1024
        )

        if file.size > max_size:
            raise serializers.ValidationError(
                "File size exceeds 5 MB."
            )

        return file