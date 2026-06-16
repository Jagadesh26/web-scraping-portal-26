from collections import Counter

from apps.jobs.models import (
    Job,
    JobMatch
)


class SkillGapService:

    @staticmethod
    def analyze(
        user
    ):

        matches = (
            JobMatch.objects.filter(
                user=user
            )
        )

        counter = Counter()

        for match in matches:

            counter.update(
                match.missing_skills
            )

        return dict(

            counter.most_common(
                20
            )

        )