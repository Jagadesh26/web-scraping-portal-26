from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.profiles.models import (
    JobRole,
    UserJobPreference
)

from apps.profiles.serializers import (
    UserJobPreferenceSerializer
)

from apps.profiles.services.job_preference import (
    JobPreferenceService
)


class JobPreferenceAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        preferences = (
            JobPreferenceService.list_preferences(
                request.user
            )
        )

        serializer = UserJobPreferenceSerializer(
            preferences,
            many=True
        )

        return Response(
            {
                "success": True,
                "message": "Preferences fetched successfully",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

    def post(self, request):

        job_role_id = request.data.get(
            "job_role_id"
        )

        is_primary = request.data.get(
            "is_primary",
            False
        )

        try:

            job_role = JobRole.objects.get(
                id=job_role_id
            )

        except JobRole.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Job role not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        preference = (
            JobPreferenceService.create_preference(
                user=request.user,
                job_role=job_role,
                is_primary=is_primary
            )
        )

        serializer = UserJobPreferenceSerializer(
            preference
        )

        return Response(
            {
                "success": True,
                "message": "Preference added successfully",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )




class JobPreferenceDeleteAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(
        self,
        request,
        id
    ):

        try:

            preference = (
                UserJobPreference.objects.get(
                    id=id,
                    user=request.user
                )
            )

        except UserJobPreference.DoesNotExist:

            return Response(
                {
                    "success": False,
                    "message": "Preference not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        JobPreferenceService.delete_preference(
            preference
        )

        return Response(
            {
                "success": True,
                "message": "Preference deleted successfully"
            },
            status=status.HTTP_200_OK
        )