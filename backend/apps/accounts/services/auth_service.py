from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

try:
    from rest_framework_simplejwt.token_blacklist.models import (
        BlacklistedToken,
        OutstandingToken,
    )
except Exception:
    BlacklistedToken = None
    OutstandingToken = None

from apps.accounts.models import (
    EmailVerificationToken,
    PasswordResetToken,
    User,
    UserSession,
)
from apps.profiles.models import Profile


class AuthService:

    PASSWORD_RESET_TOKEN_TTL = timedelta(hours=1)
    EMAIL_VERIFICATION_TOKEN_TTL = timedelta(days=1)

    @staticmethod
    @transaction.atomic
    def register_user(validated_data):

        validated_data.pop("confirm_password")

        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"]
        )

        Profile.objects.create(
            user=user
        )

        AuthService.send_verification_email(user)

        return user

    @staticmethod
    def get_tokens(user, request=None):

        refresh = RefreshToken.for_user(user)
        AuthService.create_session(user, refresh, request)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }

    @staticmethod
    def create_session(user, refresh, request=None):
        user_agent = request.META.get("HTTP_USER_AGENT", "") if request else ""
        ip_address = AuthService.get_client_ip(request) if request else None
        browser = AuthService.detect_browser(user_agent)
        device_name = AuthService.detect_device(user_agent)
        expires_at = timezone.now() + settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"]

        return UserSession.objects.create(
            user=user,
            refresh_token_jti=refresh["jti"],
            device_name=device_name,
            browser=browser,
            ip_address=ip_address,
            user_agent=user_agent,
            expires_at=expires_at,
        )

    @staticmethod
    def get_client_ip(request):
        forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")

    @staticmethod
    def detect_browser(user_agent):
        user_agent = user_agent or ""
        browser_signatures = (
            ("Edg", "Edge"),
            ("Chrome", "Chrome"),
            ("Firefox", "Firefox"),
            ("Safari", "Safari"),
            ("MSIE", "Internet Explorer"),
            ("Trident", "Internet Explorer"),
        )
        for signature, browser in browser_signatures:
            if signature in user_agent:
                return browser
        return "Unknown"

    @staticmethod
    def detect_device(user_agent):
        user_agent = (user_agent or "").lower()
        if "mobile" in user_agent or "android" in user_agent or "iphone" in user_agent:
            return "Mobile"
        if "tablet" in user_agent or "ipad" in user_agent:
            return "Tablet"
        return "Desktop"

    @staticmethod
    def send_password_reset_email(user):
        PasswordResetToken.objects.filter(
            user=user,
            used_at__isnull=True,
            expires_at__gt=timezone.now(),
        ).update(used_at=timezone.now())

        _, raw_token = PasswordResetToken.create_token(
            user=user,
            expires_at=timezone.now() + AuthService.PASSWORD_RESET_TOKEN_TTL,
        )
        reset_url = AuthService.build_frontend_url("reset-password", raw_token)

        send_mail(
            subject="Reset your password",
            message=f"Use this link to reset your password: {reset_url}",
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
            recipient_list=[user.email],
            fail_silently=True,
        )

    @staticmethod
    def send_verification_email(user):
        if user.is_verified:
            return

        EmailVerificationToken.objects.filter(
            user=user,
            used_at__isnull=True,
            expires_at__gt=timezone.now(),
        ).update(used_at=timezone.now())

        _, raw_token = EmailVerificationToken.create_token(
            user=user,
            expires_at=timezone.now() + AuthService.EMAIL_VERIFICATION_TOKEN_TTL,
        )
        verification_url = AuthService.build_frontend_url("verify-email", raw_token)

        send_mail(
            subject="Verify your email",
            message=f"Use this link to verify your email: {verification_url}",
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
            recipient_list=[user.email],
            fail_silently=True,
        )

    @staticmethod
    def build_frontend_url(path, token):
        base_url = getattr(settings, "FRONTEND_URL", "http://localhost:3000").rstrip("/")
        return f"{base_url}/{path}?token={token}"

    @staticmethod
    @transaction.atomic
    def reset_password(raw_token, password):
        token_hash = PasswordResetToken.hash_token(raw_token)
        reset_token = (
            PasswordResetToken.objects.select_for_update()
            .select_related("user")
            .filter(token_hash=token_hash)
            .first()
        )

        if not reset_token or not reset_token.is_valid:
            return False

        user = reset_token.user
        user.set_password(password)
        user.save(update_fields=("password", "updated_at"))
        reset_token.mark_used()
        AuthService.revoke_all_sessions(user)
        return True

    @staticmethod
    @transaction.atomic
    def verify_email(raw_token):
        token_hash = EmailVerificationToken.hash_token(raw_token)
        verification_token = (
            EmailVerificationToken.objects.select_for_update()
            .select_related("user")
            .filter(token_hash=token_hash)
            .first()
        )

        if not verification_token or not verification_token.is_valid:
            return False

        user = verification_token.user
        if not user.is_verified:
            user.is_verified = True
            user.save(update_fields=("is_verified", "updated_at"))
        verification_token.mark_used()
        return True

    @staticmethod
    def logout(refresh_token, user=None):
        try:
            refresh = RefreshToken(refresh_token)
            jti = refresh["jti"]
            session_qs = UserSession.objects.filter(refresh_token_jti=jti, is_active=True)
            if user is not None:
                session_qs = session_qs.filter(user=user)
            for session in session_qs:
                session.revoke()
            AuthService.blacklist_refresh_token(refresh)
            return True
        except TokenError:
            return False

    @staticmethod
    def revoke_all_sessions(user):
        now = timezone.now()
        if OutstandingToken and BlacklistedToken:
            for token in OutstandingToken.objects.filter(user=user):
                BlacklistedToken.objects.get_or_create(token=token)

        UserSession.objects.filter(user=user, is_active=True).update(
            is_active=False,
            revoked_at=now,
        )

    @staticmethod
    def revoke_session(session):
        session.revoke()
        AuthService.blacklist_refresh_token_jti(session.refresh_token_jti)

    @staticmethod
    def blacklist_refresh_token(refresh):
        try:
            refresh.blacklist()
        except AttributeError:
            AuthService.blacklist_refresh_token_jti(refresh["jti"])

    @staticmethod
    def blacklist_refresh_token_jti(jti):
        if not (OutstandingToken and BlacklistedToken):
            return

        token = OutstandingToken.objects.filter(jti=jti).first()
        if token:
            BlacklistedToken.objects.get_or_create(token=token)

    @staticmethod
    @transaction.atomic
    def change_password(user, password):
        user.set_password(password)
        user.save(update_fields=("password", "updated_at"))
        AuthService.revoke_all_sessions(user)
