from django.contrib import admin

from apps.jobs.models import (
    SearchKeyword,
)


@admin.register(
    SearchKeyword
)
class SearchKeywordAdmin(
    admin.ModelAdmin
):

    list_display = (
        "keyword",
        "is_active",
    )

    search_fields = (
        "keyword",
    )