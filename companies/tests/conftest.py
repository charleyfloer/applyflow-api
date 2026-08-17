import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from companies.models import Company


User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create_user(
        username="Jack",
        email="jack_smith@yahoo.com",
        password="Johnson767",
    )

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def company():
    return Company.objects.create(
        name="Google",
        website="https://google.com",
        location="Mountain View, CA",
    )