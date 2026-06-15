from django.urls import path

from .views import JobDetailAPIView, JobListAPIView

urlpatterns = [

    path(
        "job-list/",
        JobListAPIView.as_view(),
        name="job-list",
    ),

    path(
        "job-detail/<uuid:id>/",
        JobDetailAPIView.as_view(),
        name="job-detail",
    ),
]