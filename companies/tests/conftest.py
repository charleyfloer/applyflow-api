import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from companies.models import Company
from vacancies.models import Vacancy


User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create_user(
        username="Jack",
        email="jack_smith@yahoo.com",
        password="Johnson767",
        is_staff=True,
    )

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def regular_client(api_client):
    user = User.objects.create_user(
        username="Alex",
        email="alex@gmail.com",
        password="Alex123!",
        is_staff=False,
    )
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def company():
    return Company.objects.create(
        name="Google",
        website="https://google.com",
        location="Mountain View, CA",
    )


@pytest.fixture
def vacancy(company):
    return Vacancy.objects.create(
        company=company,
        title="Python Developer",
        description="Backend development",
    )


@pytest.fixture
def multiple_companies():
    return [
        Company.objects.create(
            name="Google",
            website="https://google.com",
            location="California",
        ),
        Company.objects.create(
            name="Microsoft",
            website="https://microsoft.com",
            location="Washington",
        ),
        Company.objects.create(
            name="Apple",
            website="https://apple.com",
            location="California",
        ),
        Company.objects.create(
            name="Amazon",
            website="https://amazon.com",
            location="Washington",
        ),
    ]
