from django.urls import path
from .views import (
    RegisterAPIView,
    CurrentUserAPIView,
    LoginAPIView,
    RefreshTokenAPIView,
)


urlpatterns = [
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path(
        "token/refresh/",
        RefreshTokenAPIView.as_view(),
        name="token_refresh",
    ),
    path("profile/", CurrentUserAPIView.as_view(), name="profile"),
]
