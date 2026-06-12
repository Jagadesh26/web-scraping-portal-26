from django.urls import path

from apps.accounts.views.register import RegisterAPIView
from apps.accounts.views.login import (
    ChangePasswordAPIView,
    CustomTokenRefreshView,
    EmailVerificationAPIView,
    ForgotPasswordAPIView,
    LoginAPIView,
    LogoutAllAPIView,
    LogoutAPIView,
    LogoutSessionAPIView,
    ResendVerificationEmailAPIView,
    ResetPasswordAPIView,
    UserSessionListAPIView,
)
from apps.accounts.views.me import CurrentUserAPIView

urlpatterns = [
    path(
        "register/",
        RegisterAPIView.as_view(),
        name="register",
    ),

    path(
        "login/",
        LoginAPIView.as_view(),
        name="login",
    ),

    path(
        "token/refresh/",
        CustomTokenRefreshView.as_view(),
        name="token-refresh",
    ),

    path(
        "forgot-password/",
        ForgotPasswordAPIView.as_view(),
        name="forgot-password",
    ),

    path(
        "reset-password/",
        ResetPasswordAPIView.as_view(),
        name="reset-password",
    ),

    path(
        "verify-email/",
        EmailVerificationAPIView.as_view(),
        name="verify-email",
    ),

    path(
        "resend-verification-email/",
        ResendVerificationEmailAPIView.as_view(),
        name="resend-verification-email",
    ),

    path(
        "logout/",
        LogoutAPIView.as_view(),
        name="logout",
    ),

    path(
        "sessions/",
        UserSessionListAPIView.as_view(),
        name="sessions",
    ),

    path(
        "sessions/<uuid:session_id>/logout/",
        LogoutSessionAPIView.as_view(),
        name="logout-session",
    ),

    path(
        "logout-all/",
        LogoutAllAPIView.as_view(),
        name="logout-all",
    ),

    path(
        "change-password/",
        ChangePasswordAPIView.as_view(),
        name="change-password",
    ),

    path(
        "me/",
        CurrentUserAPIView.as_view(),
        name="current-user",
    ),
]
