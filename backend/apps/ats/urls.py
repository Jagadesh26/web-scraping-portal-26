from django.urls import path

from .views import ATSDashboardAPIView, RecommendationAPIView, SkillGapAPIView

urlpatterns = [

    path(
        "recommendations/",
        RecommendationAPIView.as_view(),
        name="recommendations",
    ),

    path(
        "recommendation-detail/<uuid:id>/",
        RecommendationAPIView.as_view(),
        name="recommendation-detail",
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