from rest_framework import serializers

from apps.resume_checker.models import ResumeScore


class ResumeScoreSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = ResumeScore

        fields = (
            "id",
            "overall_score",
            "structure_score",
            "skills_score",
            "experience_score",
            "projects_score",
            "keyword_score",
            "strengths",
            "weaknesses",
            "recommendations",
            "created_at",
            "updated_at",
        )


class ResumeRecommendationSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = ResumeScore

        fields = (
            "strengths",
            "weaknesses",
            "recommendations",
        )

