from datetime import date

import pytest
from django.urls import reverse
from rest_framework import status

from applications.models import Application


@pytest.mark.django_db
def test_duplicate_application(
    authenticated_client,
    application,
):
    url = reverse("application-list")

    data = {
        "vacancy_id": application.vacancy.id,
        "status": Application.Status.APPLIED,
        "source": "Indeed",
        "applied_at": date.today(),
    }

    response = authenticated_client.post(
        url,
        data,
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "vacancy_id" in response.data


@pytest.mark.django_db
def test_create_application_with_invalid_status(
    authenticated_client,
    vacancy,
):
    url = reverse("application-list")

    data = {
        "vacancy_id": vacancy.id,
        "status": "test_status",
        "source": "Indeed",
        "applied_at": date.today(),
    }

    response = authenticated_client.post(
        url,
        data,
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "status" in response.data
    assert Application.objects.count() == 0


@pytest.mark.django_db
def test_create_application_without_applied_at_data(
    authenticated_client,
    vacancy,
):
    url = reverse("application-list")

    data = {
        "vacancy_id": vacancy.id,
        "status": Application.Status.APPLIED,
        "source": "Indeed",
    }

    response = authenticated_client.post(
        url,
        data,
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "applied_at" in response.data
    assert Application.objects.count() == 0


@pytest.mark.django_db
def test_saved_application_cannot_have_applied_at(
    authenticated_client,
    vacancy,
):
    response = authenticated_client.post(
        reverse("application-list"),
        {
            "vacancy_id": vacancy.id,
            "status": Application.Status.SAVED,
            "applied_at": date.today(),
        },
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "applied_at" in response.data
    assert not Application.objects.exists()