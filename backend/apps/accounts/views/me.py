from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.accounts.serializers.user import UserSerializer

class CurrentUserAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

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