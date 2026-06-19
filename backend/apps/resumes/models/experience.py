import uuid
from django.db import models

from .resume import Resume


class ResumeExperience(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name="experiences"
    )

    company_name = models.CharField(
        max_length=255
    )

    designation = models.CharField(
        max_length=255
    )

    start_date = models.DateField(
        null=True,
        blank=True
    )

    end_date = models.DateField(
        null=True,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    years_of_experience = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    class Meta:
        db_table = "resume_experiences"
