from django.urls import path

from .views import RecommendationAPIView, SkillGapAPIView

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
]