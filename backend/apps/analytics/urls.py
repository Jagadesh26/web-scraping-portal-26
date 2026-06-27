from django.urls import path

from apps.analytics.views import *

urlpatterns = [

    path(
        "overview/",
        OverviewAnalyticsAPIView.as_view(),
        name="analytics-overview",
    ),

    path(
        "jobs/",
        JobAnalyticsAPIView.as_view(),
        name="analytics-jobs",
    ),

    path(
        "resumes/",
        ResumeAnalyticsAPIView.as_view(),
        name="analytics-resumes",
    ),

    path(
        "ats/",
        ATSAnalyticsAPIView.as_view(),
        name="analytics-ats",
    ),

    path(
        "recommendations/",
        RecommendationAnalyticsAPIView.as_view(),
        name="analytics-recommendations",
    ),

    path(
        "jobs-by-source/",
        JobsBySourceAnalyticsAPIView.as_view(),
    ),

    path(
        "ats-distribution/",
        ATSDistributionAPIView.as_view(),
    ),

    path(
        "missing-skills/",
        MissingSkillsAnalyticsAPIView.as_view(),
    ),

    path(
        "top-jobs/",
        TopRecommendedJobsAPIView.as_view(),
    ),

    path(
        "collection-health/",
        CollectionHealthAPIView.as_view(),
    ),


]