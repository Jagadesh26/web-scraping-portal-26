import uuid

from django.db import models


class Skill(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    name = models.CharField(
        max_length=255,
        unique=True
    )

    category = models.CharField(
        max_length=100,
        blank=True
    )

    class Meta:
        db_table = "skills"