import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create_user(
        username="andrew",
        email="andrew@gmail.com",
        password="Testuser123!",
    )


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def access_token(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)