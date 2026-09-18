import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

from vacancies.models import Vacancy


pytestmark = pytest.mark.django_db


def test_anonymous_user_can_list_vacancies(api_client, vacancy):
    response = api_client.get(reverse("vacancy-list"))

    assert response.status_code == status.HTTP_200_OK
    assert response.data["results"][0]["id"] == vacancy.pk


def test_anonymous_user_cannot_create_vacancy(api_client, company):
    response = api_client.post(
        reverse("vacancy-list"),
        {
            "company_id": company.pk,
            "title": "Python Developer",
            "description": "Backend development",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert Vacancy.objects.count() == 0


def test_regular_user_cannot_create_vacancy(regular_client, company):
    response = regular_client.post(
        reverse("vacancy-list"),
        {
            "company_id": company.pk,
            "title": "Python Developer",
            "description": "Backend development",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Vacancy.objects.count() == 0


def test_regular_user_cannot_delete_vacancy(regular_client, vacancy):
    response = regular_client.delete(
        reverse("vacancy-detail", args=[vacancy.pk]),
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Vacancy.objects.filter(pk=vacancy.pk).exists()
