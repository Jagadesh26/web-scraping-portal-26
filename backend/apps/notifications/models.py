# apps/notifications/models.py

import uuid

from django.conf import settings
from django.db import models


class Notification(models.Model):

    TYPE_CHOICES = (

        ("SYSTEM", "SYSTEM"),

        ("RESUME", "RESUME"),

        ("ATS", "ATS"),

        ("RECOMMENDATION", "RECOMMENDATION"),

        ("JOB", "JOB"),

        ("SECURITY", "SECURITY"),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    notification_type = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES
    )

    title = models.CharField(
        max_length=255
    )

    message = models.TextField()

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        db_table = "notifications"

        ordering = [
            "-created_at"
        ]




class EmailNotification(models.Model):

    STATUS_CHOICES = (

        ("PENDING", "PENDING"),

        ("SENT", "SENT"),

        ("FAILED", "FAILED"),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    email = models.EmailField()

    subject = models.CharField(
        max_length=255
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    error_message = models.TextField(
        blank=True
    )

    sent_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        db_table = "email_notifications"

        ordering = [
            "-created_at"
        ]



