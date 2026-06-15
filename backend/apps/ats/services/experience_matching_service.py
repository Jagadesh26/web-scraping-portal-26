from apps.resumes.models import (
    ResumeAnalysis
)


class ExperienceMatchingService:

    @staticmethod
    def calculate(
        user,
        job
    ):

        analysis = (
            ResumeAnalysis.objects.filter(
                resume__user=user
            ).first()
        )

        if not analysis:

            return 0

        user_experience = (
            float(
                analysis.total_experience
            )
        )

        required_experience = (
            float(
                job.experience_min or 0
            )
        )

        if required_experience == 0:

            return 100

        if user_experience >= required_experience:

            return 100

        score = (
            user_experience
            /
            required_experience
        ) * 100

        return round(
            score,
            2
        )