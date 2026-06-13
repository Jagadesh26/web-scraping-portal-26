from apps.resumes.models import Resume
from apps.resumes.services.cloudinary_service import (
    CloudinaryService
)


class ResumeService:

    @staticmethod
    def upload_resume(
        user,
        file
    ):

        existing_resume = Resume.objects.filter(
            user=user
        ).first()

        if existing_resume:

            if existing_resume.cloudinary_public_id:

                CloudinaryService.delete_resume(
                    existing_resume.cloudinary_public_id
                )

            existing_resume.delete()

        upload_data = (
            CloudinaryService.upload_resume(
                file
            )
        )

        resume = Resume.objects.create(
            user=user,
            file_name=file.name,
            file_url=upload_data["url"],
            cloudinary_public_id=upload_data[
                "public_id"
            ],
            file_size=file.size,
            file_type=file.name.split(".")[-1],
            status="UPLOADED"
        )

        return resume

    @staticmethod
    def get_resume(user):

        return Resume.objects.filter(
            user=user
        ).first()

    @staticmethod
    def delete_resume(user):

        resume = Resume.objects.filter(
            user=user
        ).first()

        if not resume:
            return False

        if resume.cloudinary_public_id:

            CloudinaryService.delete_resume(
                resume.cloudinary_public_id
            )

        resume.delete()

        return True