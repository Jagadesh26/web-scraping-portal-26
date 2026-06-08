from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.profiles.models import JobRole
from apps.profiles.serializers import JobRoleSerializer


class JobRoleAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        queryset = JobRole.objects.all().order_by("name")

        serializer = JobRoleSerializer(
            queryset,
            many=True
        )

        return Response(
            {
                "success": True,
                "message": "Job roles fetched successfully",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )