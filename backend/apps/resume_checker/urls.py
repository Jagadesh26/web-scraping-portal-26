from django.urls import path

from apps.resume_checker.views import (
    ResumeCheckerAnalyzeAPIView,
    ResumeCheckerHistoryAPIView,
    ResumeCheckerLatestAPIView,
    ResumeCheckerMissingSkillsAPIView,
    ResumeCheckerRecommendationsAPIView,
    ResumeCheckerScoreBreakdownAPIView,
)


urlpatterns = [
    path(
        "resume-checker-latest/",
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
    path(
        "score-breakdown/",
        ResumeCheckerScoreBreakdownAPIView.as_view(),
        name="resume-checker-score-breakdown",
    ),
    path(
        "history/",
        ResumeCheckerHistoryAPIView.as_view(),
        name="resume-checker-history",
    ),
    path(
        "missing-skills/",
        ResumeCheckerMissingSkillsAPIView.as_view(),
        name="resume-checker-missing-skills",
    ),
]

