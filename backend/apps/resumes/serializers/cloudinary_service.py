import cloudinary.uploader


class CloudinaryService:

    @staticmethod
    def upload_resume(file):

        result = cloudinary.uploader.upload(
            file,
            resource_type="raw",
            folder="resumes"
        )

        return {
            "url": result["secure_url"],
            "public_id": result["public_id"]
        }

    @staticmethod
    def delete_resume(public_id):

        cloudinary.uploader.destroy(
            public_id,
            resource_type="raw"
        )