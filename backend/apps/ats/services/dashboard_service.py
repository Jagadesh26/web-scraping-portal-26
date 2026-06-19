from collections import Counter

from django.db.models import Avg
from django.db.models import Max

from apps.jobs.models import Job, JobMatch



class ATSDashboardService:

    @staticmethod
    def get_dashboard(
        user
    ):

        matches = (
            JobMatch.objects.filter(
                user=user
            )
        )

        top_matches = list(
            matches.select_related(
                "job"
            ).order_by(
                "-final_score"
            )[:10]
        )
        recent_matches = list(
            matches.select_related(
                "job"
            ).order_by(
                "-updated_at"
            )[:10]
        )
        missing_counter = Counter()
        matching_counter = Counter()

        for match in matches:
            missing_counter.update(
                match.missing_skills or []
            )
            matching_counter.update(
                match.matched_skills or []
            )

        def serialize_match(match):
            return {
                "job_id": str(
                    match.job_id
                ),
                "job_title": match.job.title,
                "company_name": match.job.company_name,
                "overall_score": match.final_score,
                "match_category": match.match_category,
                "missing_skills": match.missing_skills,
            }

        return {

            "total_jobs":
                Job.objects.filter(
                    is_active=True
                ).count(),

            "total_matches":
                matches.count(),

            "average_score":
                round(
                    matches.aggregate(
                        Avg("final_score")
                    )[
                        "final_score__avg"
                    ] or 0,
                    2
                ),

            "highest_match_score":
                round(
                    matches.aggregate(
                        Max("final_score")
                    )[
                        "final_score__max"
                    ] or 0,
                    2
                ),

            "top_matches": [
                serialize_match(
                    match
                )
                for match in top_matches
            ],

            "recently_matched_jobs": [
                serialize_match(
                    match
                )
                for match in recent_matches
            ],

            "skill_gap_analysis": [
                {
                    "skill": skill,
                    "missing_count": count,
                }
                for skill, count in missing_counter.most_common(
                    10
                )
            ],

            "most_missing_skills": [
                skill
                for skill, _ in missing_counter.most_common(
                    10
                )
            ],

            "most_common_skills": [
                skill
                for skill, _ in matching_counter.most_common(
                    10
                )
            ],
        }
