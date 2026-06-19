from apps.jobs.collectors.base import (
    BaseCollector
)


class BasePortalCollector(
    BaseCollector
):

    def get_keywords(
        self
    ):

        from apps.jobs.models import (
            SearchKeyword
        )

        return (
            SearchKeyword.objects.filter(
                is_active=True
            )
        )