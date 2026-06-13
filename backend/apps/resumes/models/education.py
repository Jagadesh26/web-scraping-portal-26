import uuid
from django.db import models

from .resume import Resume


class ResumeEducation(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name="educations"
    )

    degree = models.CharField(
        max_length=255
    )

    institution = models.CharField(
        max_length=255
    )

    start_year = models.IntegerField(
        null=True,
        blank=True
    )

    end_year = models.IntegerField(
        null=True,
        blank=True
    )

    class Meta:
        db_table = "resume_educations"