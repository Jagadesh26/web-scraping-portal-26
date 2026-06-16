from django.contrib import admin

from apps.resume_checker.models import ResumeScore


@admin.register(ResumeScore)
class ResumeScoreAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "overall_score",
        "structure_score",
        "skills_score",
        "experience_score",
        "projects_score",
        "keyword_score",
        "updated_at",
    )

    search_fields = (
        "user__email",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )
