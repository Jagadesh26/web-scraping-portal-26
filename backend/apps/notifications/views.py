# apps/notifications/views.py

from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework.permissions import (
    IsAuthenticated,
)

from rest_framework import status

from apps.notifications.models import (
    Notification
)

from apps.notifications.serializers import (
    NotificationSerializer
)
from config.authentication import ProjectJWTAuthentication



class NotificationListAPIView(
    APIView
):

    authentication_classes = [
        ProjectJWTAuthentication
    ]

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request
    ):

        notifications = (

            Notification.objects.filter(
                user=request.user
            )

            .order_by(
                "-created_at"
            )
        )

        serializer = (
            NotificationSerializer(
                notifications,
                many=True
            )
        )

        return Response(
            {
                "success": True,
                "count":
                notifications.count(),
                "data":
                serializer.data,
            }
        )




class UnreadNotificationAPIView(
    APIView
):

    authentication_classes = [
        ProjectJWTAuthentication
    ]

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request
    ):

        notifications = (

            Notification.objects.filter(
                user=request.user,
                is_read=False
            )

            .order_by(
                "-created_at"
            )
        )

        serializer = (
            NotificationSerializer(
                notifications,
                many=True
            )
        )

        return Response(
            {
                "success": True,
                "count":
                notifications.count(),
                "data":
                serializer.data,
            }
        )




class NotificationMarkReadAPIView(
    APIView
):

    authentication_classes = [
        ProjectJWTAuthentication
    ]

    permission_classes = [
        IsAuthenticated
    ]

    def patch(
        self,
        request,
        notification_id
    ):

        notification = (

            Notification.objects.filter(
                id=notification_id,
                user=request.user
            )

            .first()
        )

        if not notification:

            return Response(
                {
                    "success": False,
                    "message":
                    "Notification not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        notification.is_read = True

        notification.save(
            update_fields=[
                "is_read"
            ]
        )

        return Response(
            {
                "success": True,
                "message":
                "Notification marked as read."
            }
        )



class NotificationMarkAllReadAPIView(
    APIView
):

    authentication_classes = [
        ProjectJWTAuthentication
    ]

    permission_classes = [
        IsAuthenticated
    ]

    def patch(
        self,
        request
    ):

        Notification.objects.filter(
            user=request.user,
            is_read=False
        ).update(
            is_read=True
        )

        return Response(
            {
                "success": True,
                "message":
                "All notifications marked as read."
            }
        )




class NotificationCountAPIView(
    APIView
):

    authentication_classes = [
        ProjectJWTAuthentication
    ]

    permission_classes = [
        IsAuthenticated
    ]

    def get(
        self,
        request
    ):

        unread_count = (

            Notification.objects.filter(
                user=request.user,
                is_read=False
            )

            .count()
        )

        return Response(
            {
                "success": True,
                "unread_count":
                unread_count
            }
        )
    


