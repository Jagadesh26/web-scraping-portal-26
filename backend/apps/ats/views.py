from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated
)

from apps.ats.serializers import JobMatchDetailSerializer, JobMatchSerializer
from apps.ats.services.dashboard_service import ATSDashboardService
from apps.ats.services.skill_gap_service import SkillGapService
from apps.jobs.models import JobMatch
from config.authentication import ProjectJWTAuthentication




class RecommendationAPIView(
    APIView
):

    authentication_classes = [
        ProjectJWTAuthentication
    ]

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request
    ):

        recommendations = (
            JobMatch.objects.filter(
                user=request.user
            )
            .select_related(
                "job"
            )
            .order_by(
                "-final_score"
            )
        )

        serializer = (
            JobMatchSerializer(
                recommendations[:20],
                many=True
            )
        )

        return Response(
            {
                "success": True,
                "count": len(
                    serializer.data
                ),
                "data":
                    serializer.data,
            }
        )
    





class RecommendationDetailAPIView(
    APIView
):

    authentication_classes = [
        ProjectJWTAuthentication
    ]

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request,
        job_id
    ):

        recommendation = (
            JobMatch.objects.filter(
                user=request.user,
                job_id=job_id
            ).first()
        )

        if not recommendation:

            return Response(
                {
                    "success": False,
                    "message":
                        "Recommendation not found."
                },
                status=404
            )

        serializer = (
            JobMatchDetailSerializer(
                recommendation
            )
        )

        return Response(
            {
                "success": True,
                "data":
                    serializer.data
            }
        )
    



class MatchScoreAPIView(
    APIView
):

    authentication_classes = [
        ProjectJWTAuthentication
    ]

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request,
        job_id
    ):

        match = (
            JobMatch.objects.filter(
                user=request.user,
                job_id=job_id
            )
            .select_related(
                "job"
            )
            .first()
        )

        if not match:

            return Response(
                {
                    "success": False,
                    "message": "ATS match score not found."
                },
                status=404
            )

        return Response(
            {
                "success": True,
                "data": {
                    "overall_score": match.final_score,
                    "skill_score": match.skill_score,
                    "experience_score": match.experience_score,
                    "education_score": match.education_score,
                    "project_score": match.project_score,
                    "resume_quality_score": match.resume_quality_score,
                    "match_category": match.match_category,
                    "matching_skills": match.matched_skills,
                    "missing_skills": match.missing_skills,
                }
            }
        )


class ATSJobRecommendationAPIView(
    APIView
):

    authentication_classes = [
        ProjectJWTAuthentication
    ]

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request,
        job_id
    ):

        match = JobMatch.objects.filter(
            user=request.user,
            job_id=job_id
        ).first()

        if not match:

            return Response(
                {
                    "success": False,
                    "message": "ATS recommendations not found."
                },
                status=404
            )

        return Response(
            {
                "success": True,
                "data": {
                    "recommendations": match.recommendations,
                    "missing_skills": match.missing_skills,
                    "improvement_suggestions": match.improvement_suggestions,
                }
            }
        )


class SkillGapAPIView(
    APIView
):

    authentication_classes = [
        ProjectJWTAuthentication
    ]

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request
    ):

        data = (
            SkillGapService.analyze(
                request.user
            )
        )

        return Response(
            {
                "success": True,
                "data": data
            }
        )
    



class ATSDashboardAPIView(
    APIView
):

    authentication_classes = [
        ProjectJWTAuthentication
    ]

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request
    ):

        data = (
            ATSDashboardService
            .get_dashboard(
                request.user
            )
        )

        return Response(
            {
                "success": True,
                "data": data
            }
        )
