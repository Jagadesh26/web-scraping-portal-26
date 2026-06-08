from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.accounts.serializers.login import LoginSerializer
from apps.accounts.serializers.user import UserSerializer
from apps.accounts.services.auth_service import AuthService



class LoginAPIView(APIView):

    def post(self, request):

        serializer = LoginSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.validated_data["user"]

        tokens = AuthService.get_tokens(
            user
        )

        return Response(
            {
                "success": True,
                "message": "Login successful",
                "data": tokens
            }
        )





