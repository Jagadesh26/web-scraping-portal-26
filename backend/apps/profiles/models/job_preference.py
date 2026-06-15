import uuid

from django.db import models

from django.conf import settings

from apps.profiles.models.profile import Profile



class JobRole(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    name = models.CharField(
        max_length=255,
        unique=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = "job_roles"

    def __str__(self):
        return self.name






class UserJobPreference(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="job_preferences"
    )

    job_role = models.ForeignKey(
        JobRole,
        on_delete=models.CASCADE
    )

    is_primary = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = "user_job_preferences"
        unique_together = (
            "user",
            "job_role"
        )






class PreferredLocation(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="preferred_locations"
    )

    location = models.CharField(
        max_length=255
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        db_table = "preferred_locations"

        unique_together = (
            "profile",
            "location",
        )