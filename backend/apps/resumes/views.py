from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticated
)

from config.authentication import (
    ProjectJWTAuthentication
)

from apps.resumes.serializers.resume import (
    ResumeAnalysisSerializer,
    ResumeEducationSerializer,
    ResumeExperienceSerializer,
    ResumeProjectSerializer,
    ResumeRecommendationSerializer,
    ResumeSerializer,
    ResumeSkillSerializer,
)
from apps.resumes.serializers.resume_upload import (
    ResumeUploadSerializer
)

from apps.resumes.services.resume_service import (
    ResumeService
)
from apps.resumes.services.resume_analysis_service import (
    ResumeAnalysisService
)


from apps.resumes.models import (
    Resume,
    ResumeAnalysis,
    ResumeSkill,
    ResumeExperience,
    ResumeEducation,
    ResumeProject,
    ResumeRecommendation,
)


class ResumeUploadAPIView(APIView):

    authentication_classes = [
        ProjectJWTAuthentication
    ]

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

        ResumeAnalysisService.process_resume(
            resume,
            resume_file
        )

        resume.refresh_from_db(
            fields=["status"]
        )

        return Response(
            {
                "success": True,
                "message": "Resume uploaded successfully. Analysis generated automatically.",
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

    authentication_classes = [
        ProjectJWTAuthentication
    ]

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

    authentication_classes = [
        ProjectJWTAuthentication
    ]

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
    



class ResumeAnalysisAPIView(APIView):

    authentication_classes = [
        ProjectJWTAuthentication
    ]

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        resume = Resume.objects.filter(
            user=request.user
        ).first()

        if not resume:

            return Response(
                {
                    "success": False,
                    "message": "Resume not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        analysis = ResumeAnalysis.objects.filter(
            resume=resume
        ).first()

        if not analysis:

            return Response(
                {
                    "success": False,
                    "message": "Resume analysis not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = (
            ResumeAnalysisSerializer(
                analysis
            )
        )

        return Response(
            {
                "success": True,
                "data": serializer.data
            }
        )
    



class ResumeSkillAPIView(APIView):

    authentication_classes = [
        ProjectJWTAuthentication
    ]

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        resume = Resume.objects.filter(
            user=request.user
        ).first()

        if not resume:

            return Response(
                {
                    "success": False,
                    "message": "Resume not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        skills = ResumeSkill.objects.filter(
            resume=resume
        )

        serializer = (
            ResumeSkillSerializer(
                skills,
                many=True
            )
        )

        return Response(
            {
                "success": True,
                "data": serializer.data
            }
        )
    


class ResumeExperienceAPIView(APIView):

    authentication_classes = [
        ProjectJWTAuthentication
    ]

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        resume = Resume.objects.filter(
            user=request.user
        ).first()

        if not resume:

            return Response(
                {
                    "success": False,
                    "message": "Resume not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        experiences = (
            ResumeExperience.objects.filter(
                resume=resume
            )
        )

        serializer = (
            ResumeExperienceSerializer(
                experiences,
                many=True
            )
        )

        return Response(
            {
                "success": True,
                "data": serializer.data
            }
        )



class ResumeEducationAPIView(APIView):

    authentication_classes = [
        ProjectJWTAuthentication
    ]

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        resume = Resume.objects.filter(
            user=request.user
        ).first()

        if not resume:

            return Response(
                {
                    "success": False,
                    "message": "Resume not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        educations = (
            ResumeEducation.objects.filter(
                resume=resume
            )
        )

        serializer = (
            ResumeEducationSerializer(
                educations,
                many=True
            )
        )

        return Response(
            {
                "success": True,
                "data": serializer.data
            }
        )
    


class ResumeProjectAPIView(APIView):

    authentication_classes = [
        ProjectJWTAuthentication
    ]

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        resume = Resume.objects.filter(
            user=request.user
        ).first()

        if not resume:

            return Response(
                {
                    "success": False,
                    "message": "Resume not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        projects = (
            ResumeProject.objects.filter(
                resume=resume
            )
        )

        serializer = (
            ResumeProjectSerializer(
                projects,
                many=True
            )
        )

        return Response(
            {
                "success": True,
                "data": serializer.data
            }
        )


class ResumeRecommendationAPIView(APIView):

    authentication_classes = [
        ProjectJWTAuthentication
    ]

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        resume = Resume.objects.filter(
            user=request.user
        ).first()

        if not resume:

            return Response(
                {
                    "success": False,
                    "message": "Resume not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        recommendations = ResumeRecommendation.objects.filter(
            resume=resume
        )

        serializer = ResumeRecommendationSerializer(
            recommendations,
            many=True
        )

        return Response(
            {
                "success": True,
                "data": serializer.data
            }
        )
    


