from django.db import models

# Create your models here.



import uuid

from django.db import models

from apps.accounts.models.user import User
from apps.resumes.models.skill import Skill


class JobSource(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    name = models.CharField(
        max_length=255,
        unique=True
    )

    base_url = models.URLField()

    is_active = models.BooleanField(
        default=True
    )

    last_sync_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        db_table = "job_sources"

    def __str__(self):

        return self.name
    






class Job(models.Model):

    EMPLOYMENT_TYPES = (
        ("FULL_TIME", "FULL_TIME"),
        ("PART_TIME", "PART_TIME"),
        ("CONTRACT", "CONTRACT"),
        ("INTERNSHIP", "INTERNSHIP"),
        ("FREELANCE", "FREELANCE"),
        ("REMOTE", "REMOTE"),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    job_source = models.ForeignKey(
        JobSource,
        on_delete=models.CASCADE,
        related_name="jobs"
    )

    external_job_id = models.CharField(
        max_length=255
    )

    title = models.CharField(
        max_length=500
    )

    company_name = models.CharField(
        max_length=500
    )

    location = models.CharField(
        max_length=500,
        blank=True
    )

    employment_type = models.CharField(
        max_length=50,
        choices=EMPLOYMENT_TYPES,
        blank=True
    )

    experience_min = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        null=True,
        blank=True
    )

    experience_max = models.DecimalField(
        max_digits=5,
        decimal_places=1,
        null=True,
        blank=True
    )

    salary_min = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    salary_max = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True
    )

    currency = models.CharField(
        max_length=10,
        blank=True
    )

    description = models.TextField()

    apply_url = models.URLField()

    posted_at = models.DateTimeField(
        null=True,
        blank=True
    )

    last_seen_at = models.DateTimeField(
        null=True,
        blank=True
    )

    expires_at = models.DateTimeField(
        null=True,
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    raw_payload = models.JSONField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        db_table = "jobs"

        indexes = [
            models.Index(
                fields=["title"]
            ),

            models.Index(
                fields=["company_name"]
            ),

            models.Index(
                fields=["location"]
            ),

            models.Index(
                fields=["is_active"]
            ),

            models.Index(
                fields=["posted_at"]
            ),
        ]

        unique_together = (
            "job_source",
            "external_job_id",
        )

    def __str__(self):

        return self.title
    




class JobSkill(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="job_skills"
    )

    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name="job_skills"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        db_table = "job_skills"

        unique_together = (
            "job",
            "skill",
        )






class JobMatch(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="job_matches"
    )

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="job_matches"
    )

    skill_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    experience_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    preference_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    location_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    ai_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    final_score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    matched_skills = models.JSONField(
        default=list
    )

    missing_skills = models.JSONField(
        default=list
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        db_table = "job_matches"

        unique_together = (
            "user",
            "job",
        )