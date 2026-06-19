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


class ScoreBreakdownSerializer(
    serializers.ModelSerializer
):
    """Serializer for score breakdown endpoint."""

    class Meta:

        model = ResumeScore

        fields = (
            "overall_score",
            "structure_score",
            "skills_score",
            "experience_score",
            "projects_score",
            "keyword_score",
        )


class ResumeHistorySerializer(
    serializers.Serializer
):
    """Serializer for resume history items."""

    score = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        source="overall_score"
    )
    created_at = serializers.DateTimeField()


class MissingSkillsSerializer(
    serializers.Serializer
):
    """Serializer for missing skills endpoint."""

    missing_skills = serializers.ListField(
        child=serializers.CharField()
    )

