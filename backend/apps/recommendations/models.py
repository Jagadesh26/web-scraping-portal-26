import uuid

from django.conf import settings
from django.db import models

from apps.jobs.models import Job
from apps.resumes.models import Resume


class JobRecommendation(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="job_recommendations"
    )

    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name="job_recommendations"
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="recommendations"
    )

    match_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    matching_skills = models.JSONField(
        default=list
    )

    missing_skills = models.JSONField(
        default=list
    )

    recommendation_reason = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        db_table = "job_recommendations"

        unique_together = (
            "resume",
            "job",
        )

        ordering = (
            "-match_score",
            "-updated_at",
        )

        indexes = [
            models.Index(
                fields=[
                    "user",
                    "is_active",
                    "-match_score",
                ]
            ),
            models.Index(
                fields=[
                    "resume",
                    "is_active",
                ]
            ),
            models.Index(
                fields=[
                    "job",
                    "is_active",
                ]
            ),
        ]

    def __str__(
        self
    ):
        return f"{self.user_id} - {self.job_id} - {self.match_score}"
