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
]