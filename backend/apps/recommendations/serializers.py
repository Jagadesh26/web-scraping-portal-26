from rest_framework import serializers

from apps.recommendations.models import JobRecommendation


class JobRecommendationSerializer(serializers.ModelSerializer):

    job_id = serializers.UUIDField(
        source="job.id",
        read_only=True
    )
    job_title = serializers.CharField(
        source="job.title",
        read_only=True
    )
    company_name = serializers.CharField(
        source="job.company_name",
        read_only=True
    )
    location = serializers.CharField(
        source="job.location",
        read_only=True
    )
    apply_url = serializers.URLField(
        source="job.apply_url",
        read_only=True
    )

    class Meta:

        model = JobRecommendation

        fields = (
            "id",
            "job_id",
            "job_title",
            "company_name",
            "location",
            "apply_url",
            "match_score",
            "matching_skills",
            "missing_skills",
            "recommendation_reason",
            "created_at",
            "updated_at",
        )


class JobRecommendationDetailSerializer(JobRecommendationSerializer):

    class Meta(JobRecommendationSerializer.Meta):
        fields = JobRecommendationSerializer.Meta.fields
