"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def health_check(request):
    """Health check endpoint"""
    return JsonResponse({
        'status': 'healthy',
        'message': 'E-commerce Customer Behavior Analytics API is running'
    })


urlpatterns = [
    path("", health_check, name="health-check"),
    path("admin/", admin.site.urls),
    path("api/accounts/", include("apps.accounts.urls")),
    path("api/analytics/", include("apps.analytics.urls")),
    path("api/applications/", include("apps.applications.urls")),
    path("api/ats/", include("apps.ats.urls")),
    path("api/jobs/", include("apps.jobs.urls")),
    path("api/notifications/", include("apps.notifications.urls")),
    path("api/profiles/", include("apps.profiles.urls")),
    path("api/recommendations/", include("apps.recommendations.urls")),
    path("api/resumes/", include("apps.resumes.urls")),
    path("api/scheduler/", include("apps.scheduler.urls")),
]
