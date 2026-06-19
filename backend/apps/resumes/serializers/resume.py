from rest_framework import serializers

from apps.resumes.models import Resume
from apps.resumes.models.analysis import ResumeAnalysis
from apps.resumes.models.education import ResumeEducation
from apps.resumes.models.experience import ResumeExperience
from apps.resumes.models.project import ResumeProject
from apps.resumes.models.recommendation import ResumeRecommendation
from apps.resumes.models.resume_skill import ResumeSkill


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



class ResumeAnalysisSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = ResumeAnalysis

        fields = (
            "id",
            "summary",
            "total_experience",
            "current_designation",
            "overall_score",
            "skills_score",
            "experience_score",
            "education_score",
            "project_score",
            "keyword_score",
            "completeness_score",
            "created_at",
        )



class ResumeSkillSerializer(
    serializers.ModelSerializer
):

    skill_name = serializers.CharField(
        source="skill.name"
    )

    category = serializers.CharField(
        source="skill.category"
    )

    class Meta:

        model = ResumeSkill

        fields = (
            "id",
            "skill_name",
            "category",
            "confidence_score",
        )




class ResumeExperienceSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = ResumeExperience

        fields = (
            "id",
            "company_name",
            "designation",
            "start_date",
            "end_date",
            "years_of_experience",
            "description",
        )




class ResumeEducationSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = ResumeEducation

        fields = (
            "id",
            "degree",
            "institution",
            "start_year",
            "end_year",
        )



class ResumeProjectSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = ResumeProject

        fields = (
            "id",
            "project_name",
            "description",
            "technologies",
        )


class ResumeRecommendationSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = ResumeRecommendation

        fields = (
            "id",
            "category",
            "recommendation",
            "created_at",
        )
