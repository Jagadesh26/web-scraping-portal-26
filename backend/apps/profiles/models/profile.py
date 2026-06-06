import uuid

from django.db import models
from django.conf import settings


class Profile(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    full_name = models.CharField(
        max_length=255,
        blank=True
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    location = models.CharField(
        max_length=255,
        blank=True
    )

    current_role = models.CharField(
        max_length=255,
        blank=True
    )

    experience_years = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        default=0
    )

    linkedin_url = models.URLField(
        blank=True
    )

    github_url = models.URLField(
        blank=True
    )

    portfolio_url = models.URLField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = "profiles"

    def __str__(self):
        return self.user.email



        