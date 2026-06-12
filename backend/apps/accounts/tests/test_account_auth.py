from django.contrib.auth import get_user_model
from django.core import mail
from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import EmailVerificationToken, PasswordResetToken, UserSession


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    FRONTEND_URL="http://frontend.test",
)
class AccountAuthAPITests(APITestCase):
    password = "StrongPass123!"

    def create_user(self, email="user@example.com", password=None, **extra_fields):
        return get_user_model().objects.create_user(
            email=email,
            password=password or self.password,
            **extra_fields,
        )

    def authenticate(self, user):
        response = self.client.post(
            reverse("login"),
            {"email": user.email, "password": self.password},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {response.data['data']['access']}"
        )
        return response.data["data"]

    def test_register_creates_profile_and_verification_email(self):
        response = self.client.post(
            reverse("register"),
            {
                "email": "new@example.com",
                "password": self.password,
                "confirm_password": self.password,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email="new@example.com")
        self.assertTrue(hasattr(user, "profile"))
        self.assertEqual(EmailVerificationToken.objects.filter(user=user).count(), 1)
        self.assertEqual(len(mail.outbox), 1)

    def test_forgot_and_reset_password_use_one_time_token(self):
        user = self.create_user()

        response = self.client.post(
            reverse("forgot-password"),
            {"email": user.email},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        reset_token = PasswordResetToken.objects.get(user=user)
        raw_token = mail.outbox[0].body.split("token=")[1]
        self.assertNotEqual(reset_token.token_hash, raw_token)

        new_password = "NewStrongPass123!"
        response = self.client.post(
            reverse("reset-password"),
            {
                "token": raw_token,
                "password": new_password,
                "confirm_password": new_password,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        reset_token.refresh_from_db()
        user.refresh_from_db()
        self.assertTrue(reset_token.is_used)
        self.assertTrue(user.check_password(new_password))

        response = self.client.post(
            reverse("reset-password"),
            {
                "token": raw_token,
                "password": self.password,
                "confirm_password": self.password,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_verify_email_marks_user_verified(self):
        user = self.create_user()
        self.client.post(
            reverse("resend-verification-email"),
            {"email": user.email},
            format="json",
        )
        raw_token = mail.outbox[0].body.split("token=")[1]

        response = self.client.post(
            reverse("verify-email"),
            {"token": raw_token},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertTrue(user.is_verified)

    def test_login_creates_session_and_logout_revokes_it(self):
        user = self.create_user(is_verified=True)
        tokens = self.authenticate(user)

        session = UserSession.objects.get(user=user)
        self.assertTrue(session.is_active)

        response = self.client.get(reverse("sessions"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 1)

        response = self.client.post(
            reverse("logout"),
            {"refresh": tokens["refresh"]},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        session.refresh_from_db()
        self.assertFalse(session.is_active)

    def test_change_password_revokes_sessions(self):
        user = self.create_user(is_verified=True)
        self.authenticate(user)

        response = self.client.post(
            reverse("change-password"),
            {
                "old_password": self.password,
                "password": "ChangedPass123!",
                "confirm_password": "ChangedPass123!",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(UserSession.objects.filter(user=user, is_active=True).exists())
