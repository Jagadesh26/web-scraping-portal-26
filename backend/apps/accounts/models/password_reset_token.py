import uuid
import hashlib
import secrets

from django.db import models
from django.conf import settings
from django.utils import timezone


class PasswordResetToken(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="password_reset_tokens"
    )

    token_hash = models.CharField(
        max_length=64,
        unique=True
    )

    expires_at = models.DateTimeField()

    used_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    @staticmethod
    def hash_token(token):
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    @classmethod
    def create_token(cls, user, expires_at):
        raw_token = secrets.token_urlsafe(48)
        token = cls.objects.create(
            user=user,
            token_hash=cls.hash_token(raw_token),
            expires_at=expires_at,
        )
        return token, raw_token

    @property
    def is_used(self):
        return self.used_at is not None

    @property
    def is_expired(self):
        return timezone.now() >= self.expires_at

    @property
    def is_valid(self):
        return not self.is_used and not self.is_expired

    def mark_used(self, save=True):
        self.used_at = timezone.now()
        if save:
            self.save(update_fields=("used_at",))

    class Meta:
        db_table = "password_reset_tokens"
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=("user", "used_at")),
            models.Index(fields=("token_hash",)),
        ]
