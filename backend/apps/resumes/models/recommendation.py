import uuid

from django.db import models

from .resume import Resume


class ResumeRecommendation(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name="recommendations"
    )

    category = models.CharField(
        max_length=100
    )

    recommendation = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = "resume_recommendations"
