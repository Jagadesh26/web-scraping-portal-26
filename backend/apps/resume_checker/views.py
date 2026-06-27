from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.resume_checker.serializers import (
    MissingSkillsSerializer,
    ResumeHistorySerializer,
    ResumeRecommendationSerializer,
    ResumeScoreSerializer,
    ScoreBreakdownSerializer,
)
from apps.resume_checker.services.score_service import ResumeScoreService
from config.authentication import ProjectJWTAuthentication


class ResumeCheckerAnalyzeAPIView(
    APIView
):

    authentication_classes = [
        ProjectJWTAuthentication
    ]

    permission_classes = [
        IsAuthenticated
    ]

    def post(
        self,
        request
    ):
        score = ResumeScoreService.analyze(
            request.user
        )

        if not score:
            return Response(
                {
                    "success": False,
                    "message": "Resume not found. Upload and parse a resume first.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ResumeScoreSerializer(
            score
        )

        return Response(
            {
                "success": True,
                "message": "Resume ATS score generated successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class ResumeCheckerLatestAPIView(
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
        score = ResumeScoreService.get_latest(
            request.user
        )

        if not score:
            return Response(
                {
                    "success": False,
                    "message": "Resume ATS score not found. Run resume checker analysis first.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ResumeScoreSerializer(
            score
        )

        return Response(
            {
                "success": True,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class ResumeCheckerRecommendationsAPIView(
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
        score = ResumeScoreService.get_latest(
            request.user
        )

        if not score:
            return Response(
                {
                    "success": False,
                    "message": "Resume ATS recommendations not found. Run resume checker analysis first.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ResumeRecommendationSerializer(
            score
        )

        return Response(
            {
                "success": True,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class ResumeCheckerScoreBreakdownAPIView(
    APIView
):
    """
    Endpoint to get detailed ATS score breakdown.
    Returns overall_score, structure_score, skills_score, experience_score,
    projects_score, and keyword_score.
    """

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
        score = ResumeScoreService.get_latest(
            request.user
        )

        if not score:
            return Response(
                {
                    "success": False,
                    "message": "Score breakdown not found. Run resume checker analysis first.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ScoreBreakdownSerializer(
            score
        )

        return Response(
            {
                "success": True,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class ResumeCheckerHistoryAPIView(
    APIView
):
    """
    Endpoint to get user's resume check history.
    Returns a list of scores with timestamps to track improvement over time.
    """

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
        history = ResumeScoreService.get_history(
            request.user
        )

        if not history:
            return Response(
                {
                    "success": False,
                    "message": "No resume check history found. Run resume checker analysis first.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = ResumeHistorySerializer(
            history,
            many=True
        )

        return Response(
            {
                "success": True,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class ResumeCheckerMissingSkillsAPIView(
    APIView
):
    """
    Endpoint to get missing skills based on ATS analysis.
    Compares resume skills with market-demanded skills and returns the gap.
    """

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
        missing_skills = ResumeScoreService.get_missing_skills(
            request.user
        )

        if missing_skills is None:
            return Response(
                {
                    "success": False,
                    "message": "No resume found. Upload and parse a resume first.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = MissingSkillsSerializer(
            {
                "missing_skills": missing_skills
            }
        )

        return Response(
            {
                "success": True,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
