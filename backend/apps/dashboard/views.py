# apps/dashboard/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (
    IsAuthenticated
)

from apps.dashboard.services.dashboard_service import (
    DashboardService
)
from config.authentication import ProjectJWTAuthentication


class DashboardAPIView(APIView):

    authentication_classes = [
        ProjectJWTAuthentication
    ]

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request
    ):

        data = (
            DashboardService.get_dashboard(
                request.user
            )
        )

        return Response(
            {
                "success": True,
                "data": data,
            }
        )