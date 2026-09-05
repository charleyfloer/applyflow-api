import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from datetime import date

from companies.models import Company
from vacancies.models import Vacancy
from applications.models import Application


User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create_user(
        username="Jack",
        email="jack_smith@yahoo.com",
        password="Johnson767",
    )

@pytest.fixture
def another_user():
    return User.objects.create_user(
        username="Michael",
        email="michael@gmail.com",
        password="Asdfr123",
    )


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def another_authenticated_client(api_client, another_user):
    api_client.force_authenticate(user=another_user)
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
        description="Python backend development",
    )

@pytest.fixture
def vacancy2(company):
    return Vacancy.objects.create(
        company=company,
        title="Frontend Developer",
        description="Frontend development",
    )


@pytest.fixture
def vacancy3(company):
    return Vacancy.objects.create(
        company=company,
        title="Java Developer",
        description="Java development",
    )


@pytest.fixture
def vacancy4(company):
    return Vacancy.objects.create(
        company=company,
        title="Product Manager",
        description="Product Management",
    )


@pytest.fixture
def application(user, vacancy):
    return Application.objects.create(
        user=user,
        vacancy=vacancy,
        status=Application.Status.SAVED,
    )

@pytest.fixture
def multiple_applications(user, vacancy, vacancy2, vacancy3, vacancy4):
    return [
        Application.objects.create(
            user=user,
            vacancy=vacancy,
            status=Application.Status.APPLIED,
            applied_at=date(2026, 8, 5)
        ),
        Application.objects.create(
            user=user,
            vacancy=vacancy2,
            status=Application.Status.APPLIED,
            applied_at=date(2026, 7, 26)
        ),
        Application.objects.create(
            user=user,
            vacancy=vacancy3,
            status=Application.Status.INTERVIEW,
            applied_at=date(2026, 8, 30)
        ),
        Application.objects.create(
            user=user,
            vacancy=vacancy4,
            status=Application.Status.APPLIED,
            applied_at=date(2026, 7, 20)
        ),    
    ]