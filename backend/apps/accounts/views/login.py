from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.accounts.serializers.login import LoginSerializer, ForgotPasswordSerializer
from apps.accounts.serializers.user import UserSerializer
from apps.accounts.services.auth_service import AuthService
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenRefreshView
from apps.accounts.models.user import User
from apps.accounts.models.password_reset_token import PasswordResetToken
from django.utils import timezone
from datetime import timedelta



class LoginAPIView(APIView):

    permission_classes = [AllowAny]

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
            },status=status.HTTP_200_OK
        )






class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({
                "success": false,
                "message": "Invalid or expired refresh token"
            }, status=status.HTTP_401_UNAUTHORIZED)

        return Response({
            "success": True,
            "message": "Access token refreshed successfully",
            "data": serializer.validated_data
        }, status=status.HTTP_200_OK)







class ForgotPasswordAPIView(APIView):

    def post(self, request):

        serializer = ForgotPasswordSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        email = serializer.validated_data["email"]

        user = User.objects.filter(
            email=email
        ).first()

        if user:

            PasswordResetToken.objects.create(
                user=user,
                expires_at=timezone.now() + timedelta(hours=1)
            )

        return Response(
            {
                "success": True,
                "message": "Password reset link sent successfully."
            },
            status=status.HTTP_200_OK
        )