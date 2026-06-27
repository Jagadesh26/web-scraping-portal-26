# apps/analytics/services/analytics_service.py

from collections import Counter

from django.contrib.auth import get_user_model
from django.db.models import (
    Q,
    Avg,
    Max,
    Min,
    Count,
)

from apps.jobs.models import Job, JobSource
from apps.resumes.models import (
    Resume,
    ResumeAnalysis,
)
from apps.recommendations.models import (
    JobRecommendation,
)

User = get_user_model()


class AnalyticsService:

    @classmethod
    def get_overview(
        cls
    ):

        return {

            "total_users":
            User.objects.count(),

            "total_jobs":
            Job.objects.count(),

            "active_jobs":
            Job.objects.filter(
                is_active=True
            ).count(),

            "total_resumes":
            Resume.objects.count(),

            "total_resume_analysis":
            ResumeAnalysis.objects.count(),

            "total_recommendations":
            JobRecommendation.objects.count(),
        }

    @classmethod
    def get_job_analytics(
        cls
    ):

        return {

            "total_jobs":
            Job.objects.count(),

            "active_jobs":
            Job.objects.filter(
                is_active=True
            ).count(),

            "inactive_jobs":
            Job.objects.filter(
                is_active=False
            ).count(),
        }

    @classmethod
    def get_resume_analytics(
        cls
    ):

        return {

            "total_resumes":
            Resume.objects.count(),

            "uploaded":
            Resume.objects.filter(
                status="UPLOADED"
            ).count(),

            "processing":
            Resume.objects.filter(
                status="PROCESSING"
            ).count(),

            "completed":
            Resume.objects.filter(
                status="COMPLETED"
            ).count(),

            "failed":
            Resume.objects.filter(
                status="FAILED"
            ).count(),
        }

    @classmethod
    def get_ats_analytics(
        cls
    ):

        data = (
            ResumeAnalysis.objects.aggregate(

                average_score=Avg(
                    "overall_score"
                ),

                highest_score=Max(
                    "overall_score"
                ),

                lowest_score=Min(
                    "overall_score"
                ),
            )
        )

        return list(data)

    @classmethod
    def get_recommendation_analytics(
        cls
    ):

        data = (
            JobRecommendation.objects.aggregate(

                total=Count(
                    "id"
                ),

                average_match_score=Avg(
                    "match_score"
                ),

                highest_match_score=Max(
                    "match_score"
                ),
            )
        )

        return list(data)


    @classmethod
    def get_jobs_by_source(
        cls
    ):

        data = (
            JobSource.objects
            .annotate(
                total_jobs=Count(
                    "jobs"
                )
            )
            .values(
                "name",
                "total_jobs"
            )
            .order_by(
                "-total_jobs"
            )
        )

        return list(data)


    @classmethod
    def get_ats_distribution(cls):

        analyses = ResumeAnalysis.objects.aggregate(

            score_0_40=Count(
                "id",
                filter=Q(
                    overall_score__lte=40
                )
            ),

            score_41_60=Count(
                "id",
                filter=Q(
                    overall_score__gt=40,
                    overall_score__lte=60
                )
            ),

            score_61_80=Count(
                "id",
                filter=Q(
                    overall_score__gt=60,
                    overall_score__lte=80
                )
            ),

            score_81_100=Count(
                "id",
                filter=Q(
                    overall_score__gt=80
                )
            ),
        )

        return analyses
    
        
    @classmethod
    def get_most_missing_skills(
        cls
    ):

        recommendations = (
            JobRecommendation.objects.filter(
                is_active=True
            )
        )

        skill_counter = Counter()

        for recommendation in recommendations:

            for skill in recommendation.missing_skills:

                skill_counter[
                    skill
                ] += 1

        return [

            {
                "skill": skill,
                "count": count,
            }

            for skill, count
            in skill_counter.most_common(
                10
            )
        ]
    
    

    @classmethod
    def get_top_recommended_jobs(
        cls
    ):

        data = (

            JobRecommendation.objects

            .values(
                "job__id",
                "job__title",
                "job__company_name",
            )

            .annotate(
                recommendation_count=Count(
                    "id"
                )
            )

            .order_by(
                "-recommendation_count"
            )[:10]
        )

        return list(data)

    
    @classmethod
    def get_collection_health(
        cls
    ):

        total_sources = (
            JobSource.objects.count()
        )

        active_sources = (
            JobSource.objects.filter(
                is_active=True
            ).count()
        )

        latest_sync = (
            JobSource.objects.order_by(
                "-last_sync_at"
            ).first()
        )

        return {

            "total_sources":
            total_sources,

            "active_sources":
            active_sources,

            "inactive_sources":
            total_sources
            - active_sources,

            "latest_sync":
            latest_sync.last_sync_at
            if latest_sync
            else None,
        }




