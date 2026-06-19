from collections import Counter
from decimal import Decimal

from django.db import transaction

from apps.jobs.models import Job, JobMatch
from apps.recommendations.models import JobRecommendation
from apps.resumes.models import Resume


class JobRecommendationService:

    THRESHOLD = Decimal("40.00")

    @classmethod
    def generate_for_resume(
        cls,
        resume
    ):
        cls.remove_old_recommendations(
            resume
        )

        matches = (
            JobMatch.objects.filter(
                user=resume.user,
                job__is_active=True,
            )
            .select_related(
                "job"
            )
            .prefetch_related(
                "job__job_skills__skill"
            )
        )
        recommendations = []

        for match in matches:
            match_score = cls.calculate_match_score(
                match
            )

            if match_score < cls.THRESHOLD:
                continue

            recommendations.append(
                JobRecommendation(
                    user=resume.user,
                    resume=resume,
                    job=match.job,
                    match_score=match_score,
                    matching_skills=match.matched_skills or [],
                    missing_skills=match.missing_skills or [],
                    recommendation_reason=cls.build_recommendation_reason(
                        match,
                        match_score
                    ),
                    is_active=True,
                )
            )

        JobRecommendation.objects.bulk_create(
            recommendations,
            batch_size=1000
        )

        return {
            "resume_id": str(
                resume.id
            ),
            "total_matches": matches.count(),
            "recommendations_created": len(
                recommendations
            ),
        }

    @classmethod
    def generate_for_user(
        cls,
        user
    ):
        resume = Resume.objects.filter(
            user=user
        ).first()

        if not resume:
            return {
                "resume_id": None,
                "total_matches": 0,
                "recommendations_created": 0,
            }

        return cls.generate_for_resume(
            resume
        )

    @classmethod
    def generate_for_job(
        cls,
        job
    ):
        if not job.is_active:
            JobRecommendation.objects.filter(
                job=job
            ).update(
                is_active=False
            )

            return {
                "job_id": str(
                    job.id
                ),
                "recommendations_created": 0,
            }

        matches = (
            JobMatch.objects.filter(
                job=job,
                user__resume__isnull=False,
            )
            .select_related(
                "user",
                "job",
                "user__resume",
            )
            .prefetch_related(
                "job__job_skills__skill"
            )
        )
        recommendations = []

        with transaction.atomic():
            JobRecommendation.objects.filter(
                job=job
            ).delete()

            for match in matches:
                resume = match.user.resume
                match_score = cls.calculate_match_score(
                    match
                )

                if match_score < cls.THRESHOLD:
                    continue

                recommendations.append(
                    JobRecommendation(
                        user=match.user,
                        resume=resume,
                        job=job,
                        match_score=match_score,
                        matching_skills=match.matched_skills or [],
                        missing_skills=match.missing_skills or [],
                        recommendation_reason=cls.build_recommendation_reason(
                            match,
                            match_score
                        ),
                    )
                )

            JobRecommendation.objects.bulk_create(
                recommendations,
                batch_size=1000
            )

        return {
            "job_id": str(
                job.id
            ),
            "recommendations_created": len(
                recommendations
            ),
        }

    @staticmethod
    def remove_old_recommendations(
        resume
    ):
        JobRecommendation.objects.filter(
            resume=resume
        ).delete()

    @classmethod
    def calculate_match_score(
        cls,
        match
    ):
        job_skill_count = match.job.job_skills.count()

        if not job_skill_count:
            return Decimal("0.00")

        score = (
            Decimal(
                len(
                    match.matched_skills or []
                )
            )
            / Decimal(
                job_skill_count
            )
            * Decimal("100")
        )

        return score.quantize(
            Decimal("0.01")
        )

    @classmethod
    def build_recommendation_reason(
        cls,
        match,
        match_score
    ):
        category = cls.get_category(
            match_score
        )
        matching_skills = match.matched_skills or []
        missing_skills = match.missing_skills or []
        reasons = [
            f"{category} based on {match_score}% skill alignment."
        ]

        if matching_skills:
            reasons.append(
                "Strong "
                + ", ".join(
                    skill.title()
                    for skill in matching_skills[:3]
                )
                + " alignment."
            )

        if missing_skills:
            reasons.append(
                "Missing "
                + ", ".join(
                    skill.title()
                    for skill in missing_skills[:5]
                )
                + " skills."
            )

        if match.experience_score >= 75:
            reasons.append(
                "Experience level matches job requirements."
            )
        elif match.experience_score < 60:
            reasons.append(
                "Experience match is below the job requirement."
            )

        return " ".join(
            reasons
        )

    @staticmethod
    def get_category(
        score
    ):
        score = float(
            score
        )

        if score >= 90:
            return "Excellent Match"

        if score >= 75:
            return "Strong Match"

        if score >= 60:
            return "Good Match"

        return "Average Match"

    @staticmethod
    def get_user_recommendations(
        user
    ):
        return (
            JobRecommendation.objects.filter(
                user=user,
                is_active=True,
                job__is_active=True,
            )
            .select_related(
                "job",
                "resume",
            )
            .order_by(
                "-match_score",
                "-updated_at",
            )
        )

    @classmethod
    def get_skill_gap(
        cls,
        user
    ):
        counter = Counter()

        for missing_skills in cls.get_user_recommendations(
            user
        ).values_list(
            "missing_skills",
            flat=True
        ):
            counter.update(
                missing_skills or []
            )

        return [
            {
                "skill": skill,
                "count": count,
            }
            for skill, count in counter.most_common()
        ]
