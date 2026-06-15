from rest_framework import serializers

from apps.jobs.models import JobMatch



class JobMatchSerializer(
    serializers.ModelSerializer
):

    job_title = serializers.CharField(
        source="job.title"
    )

    company_name = serializers.CharField(
        source="job.company_name"
    )

    apply_url = serializers.URLField(
        source="job.apply_url"
    )

    class Meta:

        model = JobMatch

        fields = (
            "job_title",
            "company_name",
            "final_score",
            "matched_skills",
            "missing_skills",
            "apply_url",
        )




class JobMatchDetailSerializer(
    serializers.ModelSerializer
):

    job_title = serializers.CharField(
        source="job.title"
    )

    company_name = serializers.CharField(
        source="job.company_name"
    )

    apply_url = serializers.URLField(
        source="job.apply_url"
    )

    class Meta:

        model = JobMatch

        fields = (
            "job_title",
            "company_name",

            "skill_score",
            "experience_score",
            "preference_score",
            "location_score",
            "ai_score",

            "final_score",

            "matched_skills",
            "missing_skills",

            "apply_url",
        )