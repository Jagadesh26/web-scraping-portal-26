from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.resume_checker.serializers import (
    ResumeRecommendationSerializer,
    ResumeScoreSerializer,
)
from apps.resume_checker.services.score_service import ResumeScoreService


class ResumeCheckerAnalyzeAPIView(
    APIView
):

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
