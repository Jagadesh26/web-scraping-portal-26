import uuid

from django.db import models
from django.conf import settings


class Resume(models.Model):

    STATUS_CHOICES = (
        ("UPLOADED", "UPLOADED"),
        ("PROCESSING", "PROCESSING"),
        ("COMPLETED", "COMPLETED"),
        ("FAILED", "FAILED"),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="resume"
    )

    file_name = models.CharField(
        max_length=255
    )

    file_url = models.URLField()

    file_size = models.BigIntegerField()

    file_type = models.CharField(
        max_length=20
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="UPLOADED"
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    cloudinary_public_id = models.CharField(
            max_length=500,
            blank=True,
            null=True
        )

    class Meta:
        db_table = "resumes"