from django.urls import path

from .views import (
    ATSDashboardAPIView,
    ATSJobRecommendationAPIView,
    MatchScoreAPIView,
    RecommendationAPIView,
    RecommendationDetailAPIView,
    SkillGapAPIView,
)

urlpatterns = [

    path(
        "recommendations/",
        RecommendationAPIView.as_view(),
        name="recommendations",
    ),

    path(
        "recommendation-detail/<uuid:job_id>/",
        RecommendationDetailAPIView.as_view(),
        name="recommendation-detail",
    ),

    path(
        "match-score/<uuid:job_id>/",
        MatchScoreAPIView.as_view(),
        name="ats-match-score",
    ),

    path(
        "recommendations/<uuid:job_id>/",
        ATSJobRecommendationAPIView.as_view(),
        name="ats-job-recommendations",
    ),

    path(
        "skill-gap/",
        SkillGapAPIView.as_view(),
        name="skill-gap",
    ),

    path(
        "dashboard/",
        ATSDashboardAPIView.as_view(),
        name="ats-dashboard",
    ),
]
