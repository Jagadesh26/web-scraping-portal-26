from django.urls import path

from .views import *

urlpatterns = [

    path(
        "upload/",
        ResumeUploadAPIView.as_view(),
        name="resume-upload"
    ),

    path(
        "resume-view/",
        ResumeAPIView.as_view(),
        name="resume-detail"
    ),

    path(
        "delete/",
        ResumeDeleteAPIView.as_view(),
        name="resume-delete"
    ),

     path(
        "analysis/",
        ResumeAnalysisAPIView.as_view(),
        name="resume-analysis",
    ),

    path(
        "skills/",
        ResumeSkillAPIView.as_view(),
        name="resume-skills",
    ),

    path(
        "experience/",
        ResumeExperienceAPIView.as_view(),
        name="resume-experience",
    ),

    path(
        "education/",
        ResumeEducationAPIView.as_view(),
        name="resume-education",
    ),

    path(
        "projects/",
        ResumeProjectAPIView.as_view(),
        name="resume-projects",
    ),
]