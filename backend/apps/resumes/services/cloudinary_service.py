import cloudinary
import cloudinary.uploader
from django.conf import settings


cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
    secure=True
)


class CloudinaryService:

    @staticmethod
    def upload_resume(file):

        if hasattr(file, "seek"):
            file.seek(0)

        result = cloudinary.uploader.upload(
            file,
            resource_type="raw",
            folder="resumes"
        )

        if hasattr(file, "seek"):
            file.seek(0)

        return {
            "url": result["secure_url"],
            "public_id": result["public_id"]
        }

    @staticmethod
    def delete_resume(public_id):

        if not public_id:
            return None

        return cloudinary.uploader.destroy(
            public_id,
            resource_type="raw"
        )
