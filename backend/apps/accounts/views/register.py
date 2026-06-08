from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from apps.accounts.serializers import RegisterSerializer
from apps.accounts.services.auth_service import AuthService


class RegisterAPIView(APIView):

    def post(self, request):

        serializer = RegisterSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = AuthService.register_user(
            serializer.validated_data
        )

        return Response(
            {
                "success": True,
                "message": "Registration successful",
                "data": {
                    "user_id": str(user.id),
                    "email": user.email
                }
            },
            status=status.HTTP_201_CREATED
        )