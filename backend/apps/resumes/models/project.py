import uuid
from django.db import models

from .resume import Resume


class ResumeProject(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name="projects"
    )

    project_name = models.CharField(
        max_length=255
    )

    description = models.TextField(
        blank=True
    )

    technologies = models.TextField(
        blank=True
    )

    class Meta:
        db_table = "resume_projects"