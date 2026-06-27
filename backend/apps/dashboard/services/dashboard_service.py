# apps/dashboard/services/dashboard_service.py

from django.db.models import Avg, Max, Count

from apps.jobs.models import Job
from apps.recommendations.models import JobRecommendation
from apps.resumes.models import (
    Resume,
    ResumeAnalysis,
)


class DashboardService:

    @classmethod
    def get_dashboard(
        cls,
        user
    ):

        resume = (
            Resume.objects.filter(
                user=user
            )
            .select_related("analysis")
            .first()
        )

        analysis = None

        if resume:

            analysis = getattr(
                resume,
                "analysis",
                None
            )

        recommendations = (
            JobRecommendation.objects.filter(
                user=user,
                is_active=True
            )
            .select_related("job")
        )

        recommendation_stats = (
            recommendations.aggregate(
                total=Count("id"),
                average_score=Avg(
                    "match_score"
                ),
                top_score=Max(
                    "match_score"
                ),
            )
        )

        top_jobs = (
            recommendations.order_by(
                "-match_score"
            )[:5]
        )

        missing_skills = {}

        for rec in recommendations:

            for skill in rec.missing_skills:

                missing_skills[
                    skill
                ] = (
                    missing_skills.get(
                        skill,
                        0
                    ) + 1
                )

        skill_gap = sorted(
            missing_skills.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]

        total_jobs = (
            Job.objects.filter(
                is_active=True
            ).count()
        )

        return {

            "profile": {

                "name": getattr(
                    user,
                    "full_name",
                    ""
                ),

                "email": user.email,
            },

            "resume": {

                "uploaded": bool(
                    resume
                ),

                "status":
                resume.status
                if resume else None,

                "uploaded_at":
                resume.uploaded_at
                if resume else None,
            },

            "ats": {

                "overall_score":
                analysis.overall_score
                if analysis else 0,

                "skills_score":
                analysis.skills_score
                if analysis else 0,

                "experience_score":
                analysis.experience_score
                if analysis else 0,

                "education_score":
                analysis.education_score
                if analysis else 0,

                "project_score":
                analysis.project_score
                if analysis else 0,
            },

            "recommendations": {

                "total":
                recommendation_stats[
                    "total"
                ] or 0,

                "average_score":
                recommendation_stats[
                    "average_score"
                ] or 0,

                "top_score":
                recommendation_stats[
                    "top_score"
                ] or 0,
            },

            "top_jobs": [

                {
                    "job_id":
                    str(rec.job.id),

                    "title":
                    rec.job.title,

                    "company":
                    rec.job.company_name,

                    "location":
                    rec.job.location,

                    "match_score":
                    rec.match_score,
                }

                for rec in top_jobs
            ],

            "skill_gap": [

                {
                    "skill": skill,
                    "count": count,
                }

                for skill, count
                in skill_gap
            ],

            "job_market": {

                "total_active_jobs":
                total_jobs,
            },
        }