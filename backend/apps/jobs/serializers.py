from rest_framework import serializers

from apps.jobs.models import Job


class JobSerializer(
    serializers.ModelSerializer
):

    source_name = serializers.CharField(
        source="job_source.name",
        read_only=True
    )

    class Meta:

        model = Job

        fields = (
            "id",
            "title",
            "company_name",
            "location",
            "employment_type",
            "experience_min",
            "experience_max",
            "salary_min",
            "salary_max",
            "currency",
            "apply_url",
            "posted_at",
            "source_name",
        )





class JobDetailSerializer(
    serializers.ModelSerializer
):

    source_name = serializers.CharField(
        source="job_source.name",
        read_only=True
    )

    class Meta:

        model = Job

        fields = (
            "id",
            "title",
            "company_name",
            "location",
            "employment_type",
            "experience_min",
            "experience_max",
            "salary_min",
            "salary_max",
            "currency",
            "description",
            "apply_url",
            "posted_at",
            "source_name",
            "created_at",
        )