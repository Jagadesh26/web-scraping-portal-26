from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from apps.accounts.serializers.user import UserSerializer
from config.authentication import ProjectJWTAuthentication

class CurrentUserAPIView(APIView):

    authentication_classes = [
        ProjectJWTAuthentication
    ]

    permission_classes = [
        IsAuthenticated
    ]

    @extend_schema(
        responses={200: UserSerializer},
        tags=["Accounts"],
    )
    def get(self, request):

        serializer = UserSerializer(
            request.user
        )

        return Response(
            {
                "success": True,
                "data": serializer.data
            }
        )
