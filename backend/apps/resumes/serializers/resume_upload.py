from rest_framework import serializers
from django.conf import settings


class ResumeUploadSerializer(serializers.Serializer):

    resume = serializers.FileField()

    def validate_resume(self, file):

        file_name = file.name or ""

        if "." not in file_name:
            raise serializers.ValidationError(
                "Only PDF and DOCX files are allowed."
            )

        extension = file_name.rsplit(".", 1)[-1].lower()

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
                f"File size exceeds {settings.MAX_RESUME_SIZE_MB} MB."
            )

        return file
