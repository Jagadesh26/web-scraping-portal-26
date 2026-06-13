from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticated
)

from apps.resumes.serializers.resume import ResumeSerializer
from apps.resumes.serializers.resume_upload import (
    ResumeUploadSerializer
)

from apps.resumes.services.resume_service import (
    ResumeService
)


class ResumeUploadAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def post(self, request):

        serializer = (
            ResumeUploadSerializer(
                data=request.data
            )
        )

        serializer.is_valid(
            raise_exception=True
        )

        resume_file = (
            serializer.validated_data[
                "resume"
            ]
        )

        resume = (
            ResumeService.upload_resume(
                request.user,
                resume_file
            )
        )

        return Response(
            {
                "success": True,
                "message": "Resume uploaded successfully.",
                "data": {
                    "resume_id": str(
                        resume.id
                    ),
                    "file_url": resume.file_url,
                    "status": resume.status,
                }
            },
            status=status.HTTP_201_CREATED
        )




class ResumeAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        resume = (
            ResumeService.get_resume(
                request.user
            )
        )

        if not resume:

            return Response(
                {
                    "success": False,
                    "message": "Resume not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ResumeSerializer(
            resume
        )

        return Response(
            {
                "success": True,
                "data": serializer.data
            }
        )
    


class ResumeDeleteAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def delete(self, request):

        deleted = (
            ResumeService.delete_resume(
                request.user
            )
        )

        if not deleted:

            return Response(
                {
                    "success": False,
                    "message": "Resume not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {
                "success": True,
                "message": "Resume deleted successfully."
            },
            status=status.HTTP_200_OK
        )