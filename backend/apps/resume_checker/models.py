import uuid

from django.conf import settings
from django.db import models


class ResumeScore(
    models.Model
):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="resume_scores",
    )

    overall_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )

    structure_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )

    skills_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )

    experience_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )

    projects_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )

    keyword_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )

    strengths = models.JSONField(
        default=list,
        blank=True,
    )

    weaknesses = models.JSONField(
        default=list,
        blank=True,
    )

    recommendations = models.JSONField(
        default=list,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:

        db_table = "resume_scores"

    def __str__(self):
        return f"{self.user} - {self.overall_score}"
