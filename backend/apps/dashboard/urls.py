# apps/dashboard/urls.py

from django.urls import path

from apps.dashboard.views import (
    DashboardAPIView
)

urlpatterns = [

    path(
        "dashboard-detail/",
        DashboardAPIView.as_view(),
        name="dashboard"
    ),
]