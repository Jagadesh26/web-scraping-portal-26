# apps/analytics/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated,
)

from apps.analytics.services import AnalyticsService
from config.authentication import ProjectJWTAuthentication



class OverviewAnalyticsAPIView(
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

        return Response(
            {
                "success": True,
                "data":
                AnalyticsService.get_overview()
            }
        )
    



class JobAnalyticsAPIView(
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

        return Response(
            {
                "success": True,
                "data":
                AnalyticsService.get_job_analytics()
            }
        )
    



class ResumeAnalyticsAPIView(
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

        return Response(
            {
                "success": True,
                "data":
                AnalyticsService.get_resume_analytics()
            }
        )




class ATSAnalyticsAPIView(
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

        return Response(
            {
                "success": True,
                "data":
                AnalyticsService.get_ats_analytics()
            }
        )
    



class RecommendationAnalyticsAPIView(
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

        return Response(
            {
                "success": True,
                "data":
                AnalyticsService.get_recommendation_analytics()
            }
        )



class JobsBySourceAnalyticsAPIView(
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

        return Response(
            {
                "success": True,
                "data":
                AnalyticsService
                .get_jobs_by_source()
            }
        )



class ATSDistributionAPIView(
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

        return Response(
            {
                "success": True,
                "data":
                AnalyticsService
                .get_ats_distribution()
            }
        )
    


class MissingSkillsAnalyticsAPIView(
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

        return Response(
            {
                "success": True,
                "data":
                AnalyticsService
                .get_most_missing_skills()
            }
        )



class TopRecommendedJobsAPIView(
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

        return Response(
            {
                "success": True,
                "data":
                AnalyticsService
                .get_top_recommended_jobs()
            }
        )




class CollectionHealthAPIView(
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

        return Response(
            {
                "success": True,
                "data":
                AnalyticsService
                .get_collection_health()
            }
        )


        


