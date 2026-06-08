from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class ProfileAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):
        pass

    def patch(self, request):
        pass