import uuid

from django.db import models
from django.conf import settings


class UserSession(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sessions"
    )

    refresh_token_jti = models.CharField(
        max_length=255,
        unique=True
    )

    device_name = models.CharField(
        max_length=255,
        blank=True
    )

    browser = models.CharField(
        max_length=255,
        blank=True
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    user_agent = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    last_activity = models.DateTimeField(
        auto_now=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = "user_sessions"