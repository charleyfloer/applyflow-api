import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from companies.models import Company
from vacancies.models import EmploymentType, Vacancy


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


@pytest.fixture
def another_company():
    return Company.objects.create(
        name="Microsoft",
        website="https://microsoft.com",
        location="Redmond, WA",
    )


@pytest.fixture
def vacancy(company):
    return Vacancy.objects.create(
        company=company,
        title="Python Developer",
        description="Backend development",
        website="https://google.com/jobs/python",
        location="Remote",
        employment_type=EmploymentType.FULL_TIME,
        salary_min="100000.00",
        salary_max="150000.00",
    )


