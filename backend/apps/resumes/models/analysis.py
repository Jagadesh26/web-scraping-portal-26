import uuid
from django.db import models

from .resume import Resume


class ResumeAnalysis(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    resume = models.OneToOneField(
        Resume,
        on_delete=models.CASCADE,
        related_name="analysis"
    )

    raw_text = models.TextField()

    summary = models.TextField(
        blank=True
    )

    total_experience = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        default=0
    )

    current_designation = models.CharField(
        max_length=255,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = "resume_analysis"