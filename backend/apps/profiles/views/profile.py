from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from config.authentication import ProjectJWTAuthentication

class ProfileAPIView(APIView):

    authentication_classes = [
        ProjectJWTAuthentication
    ]

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):
        pass

    def patch(self, request):
        pass