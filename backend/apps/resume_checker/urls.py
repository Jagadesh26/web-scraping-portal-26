from django.urls import path

from apps.resume_checker.views import (
    ResumeCheckerAnalyzeAPIView,
    ResumeCheckerLatestAPIView,
    ResumeCheckerRecommendationsAPIView,
)


urlpatterns = [
    path(
        "",
        ResumeCheckerLatestAPIView.as_view(),
        name="resume-checker-latest",
    ),
    path(
        "analyze/",
        ResumeCheckerAnalyzeAPIView.as_view(),
        name="resume-checker-analyze",
    ),
    path(
        "recommendations/",
        ResumeCheckerRecommendationsAPIView.as_view(),
        name="resume-checker-recommendations",
    ),
]

