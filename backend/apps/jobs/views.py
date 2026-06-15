from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (
    AllowAny
)

from apps.jobs.models import Job, JobSkill
from apps.jobs.serializers import JobDetailSerializer, JobSerializer



class JobListAPIView(APIView):

    permission_classes = [
        AllowAny
    ]

    def get(self, request):

        queryset = Job.objects.filter(
            is_active=True
        )

        title = request.GET.get(
            "title"
        )

        location = request.GET.get(
            "location"
        )

        company = request.GET.get(
            "company"
        )

        employment_type = request.GET.get(
            "employment_type"
        )

        skills = request.GET.get(
            "skills"
        )

        

        if title:

            queryset = queryset.filter(
                title__icontains=title
            )

        if location:

            queryset = queryset.filter(
                location__icontains=location
            )

        if company:

            queryset = queryset.filter(
                company_name__icontains=company
            )

        if employment_type:

            queryset = queryset.filter(
                employment_type=employment_type
            )

        if skills:

            queryset = JobSkill.objects.filter(
                    job=queryset,
                    skill__name__in=skills.split(",")
            )

        queryset = queryset.order_by(
            "-posted_at",
            "-created_at"
        )

        page = int(
            request.GET.get(
                "page",
                1
            )
        )

        page_size = int(
            request.GET.get(
                "page_size",
                20
            )
        )

        start = (
            page - 1
        ) * page_size

        end = start + page_size

        total = queryset.count()

        jobs = queryset[
            start:end
        ]

        serializer = (
            JobSerializer(
                jobs,
                many=True
            )
        )

        return Response(
            {
                "success": True,
                "total": total,
                "page": page,
                "page_size": page_size,
                "data": serializer.data,
            }
        )
    






class JobDetailAPIView(APIView):

    permission_classes = [
        AllowAny
    ]

    def get(
        self,
        request,
        id
    ):

        job = Job.objects.filter(
            id=id,
            is_active=True
        ).first()

        if not job:

            return Response(
                {
                    "success": False,
                    "message": "Job not found."
                },
                status=404
            )

        serializer = (
            JobDetailSerializer(
                job
            )
        )

        return Response(
            {
                "success": True,
                "data": serializer.data
            }
        )