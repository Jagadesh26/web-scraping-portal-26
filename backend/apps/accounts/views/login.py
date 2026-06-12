from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.utils import OpenApiResponse, extend_schema

from apps.accounts.models import User
from apps.accounts.serializers.login import (
    ChangePasswordSerializer,
    EmailVerificationSerializer,
    ForgotPasswordSerializer,
    LoginSerializer,
    LogoutAllSerializer,
    LogoutSerializer,
    ResendVerificationEmailSerializer,
    ResetPasswordSerializer,
    UserSessionSerializer,
)
from apps.accounts.services.auth_service import AuthService



class LoginAPIView(APIView):

    permission_classes = [AllowAny]

    @extend_schema(
        request=LoginSerializer,
        responses={200: OpenApiResponse(description="Login successful")},
        tags=["Accounts"],
    )
    def post(self, request):

        serializer = LoginSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        user = serializer.validated_data["user"]

        tokens = AuthService.get_tokens(
            user,
            request=request,
        )

        return Response(
            {
                "success": True,
                "message": "Login successful",
                "data": tokens
            },
            status=status.HTTP_200_OK
        )






class CustomTokenRefreshView(TokenRefreshView):
    @extend_schema(tags=["Accounts"])
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({
                "success": False,
                "message": "Invalid or expired refresh token"
            }, status=status.HTTP_401_UNAUTHORIZED)

        return Response({
            "success": True,
            "message": "Access token refreshed successfully",
            "data": serializer.validated_data
        }, status=status.HTTP_200_OK)







class ForgotPasswordAPIView(APIView):

    permission_classes = [AllowAny]

    @extend_schema(
        request=ForgotPasswordSerializer,
        responses={200: OpenApiResponse(description="Password reset email sent if the account exists")},
        tags=["Accounts"],
    )
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

        if user and user.is_active:
            AuthService.send_password_reset_email(user)

        return Response(
            {
                "success": True,
                "message": "If an account exists for this email, a password reset link has been sent."
            },
            status=status.HTTP_200_OK
        )


class ResetPasswordAPIView(APIView):

    permission_classes = [AllowAny]

    @extend_schema(
        request=ResetPasswordSerializer,
        responses={
            200: OpenApiResponse(description="Password reset successful"),
            400: OpenApiResponse(description="Invalid or expired reset token"),
        },
        tags=["Accounts"],
    )
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        success = AuthService.reset_password(
            serializer.validated_data["token"],
            serializer.validated_data["password"],
        )

        if not success:
            return Response(
                {
                    "success": False,
                    "message": "Invalid or expired password reset token.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "success": True,
                "message": "Password reset successfully.",
            },
            status=status.HTTP_200_OK,
        )


class EmailVerificationAPIView(APIView):

    permission_classes = [AllowAny]

    @extend_schema(
        request=EmailVerificationSerializer,
        responses={
            200: OpenApiResponse(description="Email verified"),
            400: OpenApiResponse(description="Invalid or expired verification token"),
        },
        tags=["Accounts"],
    )
    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        success = AuthService.verify_email(serializer.validated_data["token"])
        if not success:
            return Response(
                {
                    "success": False,
                    "message": "Invalid or expired email verification token.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "success": True,
                "message": "Email verified successfully.",
            },
            status=status.HTTP_200_OK,
        )


class ResendVerificationEmailAPIView(APIView):

    permission_classes = [AllowAny]

    @extend_schema(
        request=ResendVerificationEmailSerializer,
        responses={200: OpenApiResponse(description="Verification email sent if needed")},
        tags=["Accounts"],
    )
    def post(self, request):
        serializer = ResendVerificationEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.filter(email=serializer.validated_data["email"]).first()
        if user and user.is_active and not user.is_verified:
            AuthService.send_verification_email(user)

        return Response(
            {
                "success": True,
                "message": "If verification is required, a verification email has been sent.",
            },
            status=status.HTTP_200_OK,
        )


class LogoutAPIView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=LogoutSerializer,
        responses={200: OpenApiResponse(description="Logged out")},
        tags=["Accounts"],
    )
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        success = AuthService.logout(serializer.validated_data["refresh"], request.user)
        if not success:
            return Response(
                {
                    "success": False,
                    "message": "Invalid refresh token.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "success": True,
                "message": "Logged out successfully.",
            },
            status=status.HTTP_200_OK,
        )


class UserSessionListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: UserSessionSerializer(many=True)},
        tags=["Accounts"],
    )
    def get(self, request):
        sessions = request.user.sessions.filter(is_active=True)
        serializer = UserSessionSerializer(sessions, many=True)
        return Response(
            {
                "success": True,
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class LogoutSessionAPIView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: OpenApiResponse(description="Session revoked")},
        tags=["Accounts"],
    )
    def delete(self, request, session_id):
        session = request.user.sessions.filter(id=session_id, is_active=True).first()
        if not session:
            return Response(
                {
                    "success": False,
                    "message": "Session not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        AuthService.revoke_session(session)
        return Response(
            {
                "success": True,
                "message": "Session logged out successfully.",
            },
            status=status.HTTP_200_OK,
        )


class LogoutAllAPIView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=LogoutAllSerializer,
        responses={200: OpenApiResponse(description="All sessions revoked")},
        tags=["Accounts"],
    )
    def post(self, request):
        AuthService.revoke_all_sessions(request.user)
        return Response(
            {
                "success": True,
                "message": "Logged out from all sessions successfully.",
            },
            status=status.HTTP_200_OK,
        )


class ChangePasswordAPIView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=ChangePasswordSerializer,
        responses={200: OpenApiResponse(description="Password changed")},
        tags=["Accounts"],
    )
    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)

        AuthService.change_password(request.user, serializer.validated_data["password"])
        return Response(
            {
                "success": True,
                "message": "Password changed successfully. Please log in again.",
            },
            status=status.HTTP_200_OK,
        )
