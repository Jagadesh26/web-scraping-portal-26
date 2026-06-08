from django.urls import path

from apps.accounts.views.register import RegisterAPIView
from apps.accounts.views.login import LoginAPIView
from apps.accounts.views.me import CurrentUserAPIView

urlpatterns = [
    path(
        "register/",
        RegisterAPIView.as_view(),
        name="register",
    ),

    path(
        "login/",
        LoginAPIView.as_view(),
        name="login",
    ),

    path(
        "me/",
        CurrentUserAPIView.as_view(),
        name="current-user",
    ),
]