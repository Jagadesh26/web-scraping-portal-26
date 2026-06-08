from django.urls import path

from apps.profiles.views.profile import ProfileAPIView
from apps.profiles.views.job_role import JobRoleAPIView
from apps.profiles.views.job_preference import (
    JobPreferenceAPIView,
    JobPreferenceDeleteAPIView,
)

urlpatterns = [

    path(
        "",
        ProfileAPIView.as_view(),
        name="profile",
    ),

    path(
        "job-preferences/",
        JobPreferenceAPIView.as_view(),
        name="job-preferences",
    ),

    path(
        "job-preferences/<uuid:id>/",
        JobPreferenceDeleteAPIView.as_view(),
        name="job-preference-delete",
    ),
]

urlpatterns += [
    path(
        "../job-roles/",
        JobRoleAPIView.as_view(),
        name="job-roles",
    ),
]