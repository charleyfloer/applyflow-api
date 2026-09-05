import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APIClient

from companies.models import Company
from vacancies.models import Vacancy
from applications.models import Application
from interviews.models import Interview


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
def application(user, vacancy):
    return Application.objects.create(
        user=user,
        vacancy=vacancy,
        status=Application.Status.SAVED,
    )


@pytest.fixture
def application2(user, vacancy2):
    return Application.objects.create(
        user=user,
        vacancy=vacancy2,
        status=Application.Status.APPLIED,
    )


@pytest.fixture
def another_application(another_user, vacancy2):
    return Application.objects.create(
        user=another_user,
        vacancy=vacancy2,
        status=Application.Status.SAVED,
    )


@pytest.fixture
def interview(application):
    return Interview.objects.create(
        application=application,
        type=Interview.Type.HR,
        scheduled_at=timezone.now(),
        result=Interview.Result.PENDING,
    )


@pytest.fixture
def another_interview(another_application):
    return Interview.objects.create(
        application=another_application,
        type=Interview.Type.TECHNICAL,
        scheduled_at=timezone.now(),
        result=Interview.Result.PENDING,
    )


@pytest.fixture
def multiple_interviews(application, application2):
    now = timezone.now()

    return [
        Interview.objects.create(
            application=application,
            type=Interview.Type.HR,
            scheduled_at=now - timedelta(days=7),
            result=Interview.Result.PASSED,
            notes="HR interview completed",
        ),
        Interview.objects.create(
            application=application,
            type=Interview.Type.TECHNICAL,
            scheduled_at=now - timedelta(days=3),
            result=Interview.Result.PASSED,
            notes="Django technical interview completed",
        ),
        Interview.objects.create(
            application=application,
            type=Interview.Type.FINAL,
            scheduled_at=now + timedelta(days=1),
            result=Interview.Result.PENDING,
            notes="Need to prepare for final interview",
        ),
        Interview.objects.create(
            application=application2,
            type=Interview.Type.TECHNICAL,
            scheduled_at=now - timedelta(days=4),
            result=Interview.Result.FAILED,
            notes="Technical interview failed",
        ),
    ]