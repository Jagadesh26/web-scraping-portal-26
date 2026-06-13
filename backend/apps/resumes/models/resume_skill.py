import uuid

from django.db import models

from .resume import Resume
from .skill import Skill


class ResumeSkill(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    resume = models.ForeignKey(
        Resume,
        on_delete=models.CASCADE,
        related_name="skills"
    )

    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE
    )

    confidence_score = models.FloatField(
        default=0
    )

    class Meta:
        db_table = "resume_skills"