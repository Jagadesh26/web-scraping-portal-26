# apps/notifications/urls.py

from django.urls import path

from apps.notifications.views import (

    NotificationListAPIView,

    UnreadNotificationAPIView,

    NotificationMarkReadAPIView,

    NotificationMarkAllReadAPIView,

    NotificationCountAPIView,
)

urlpatterns = [

    path(
        "",
        NotificationListAPIView.as_view(),
        name="notification-list",
    ),

    path(
        "unread/",
        UnreadNotificationAPIView.as_view(),
        name="notification-unread",
    ),

    path(
        "count/",
        NotificationCountAPIView.as_view(),
        name="notification-count",
    ),

    path(
        "<uuid:notification_id>/read/",
        NotificationMarkReadAPIView.as_view(),
        name="notification-read",
    ),

    path(
        "read-all/",
        NotificationMarkAllReadAPIView.as_view(),
        name="notification-read-all",
    ),
]