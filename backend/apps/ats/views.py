from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated
)

from apps.ats.serializers import JobMatchDetailSerializer, JobMatchSerializer
from apps.ats.services.recommendation_service import (
    RecommendationService
)
from apps.ats.services.skill_gap_service import SkillGapService
from apps.jobs.models import JobMatch




class RecommendationAPIView(
    APIView
):

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request
    ):

        recommendations = (
            RecommendationService.generate(
                request.user
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
    



class SkillGapAPIView(
    APIView
):

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