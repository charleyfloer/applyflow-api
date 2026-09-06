from datetime import date

import pytest
from django.urls import reverse
from rest_framework import status

from applications.models import Application


@pytest.mark.django_db
def test_create_application_with_nested_vacancy_representation(
    authenticated_client,
    vacancy,
    user,
):
    url = reverse("application-list")

    data = {
        "vacancy_id": vacancy.id,
        "status": Application.Status.APPLIED,
        "source": "LinkedIn",
        "applied_at": date.today(),
    }

    response = authenticated_client.post(
        url,
        data,
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert Application.objects.count() == 1

    application = Application.objects.get(pk=response.data["id"])

    assert application.user == user
    assert application.vacancy == vacancy
    assert application.status == Application.Status.APPLIED
    assert application.source == "LinkedIn"
    assert application.applied_at == date.today()
    
    assert response.data["vacancy"]["id"] == vacancy.id
    assert response.data["vacancy"]["title"] == vacancy.title
    assert response.data["vacancy"]["description"] == vacancy.description


@pytest.mark.django_db
def test_retrieve_application_with_nested_vacancy(
    authenticated_client,
    application,
):
    url = reverse("application-detail", args=[application.id])

    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    assert response.data["id"] == application.id
    assert response.data["status"] == application.status

    assert response.data["vacancy"]["id"] == application.vacancy.id
    assert response.data["vacancy"]["title"] == application.vacancy.title
    assert response.data["vacancy"]["description"] == application.vacancy.description


@pytest.mark.django_db
def test_list_multiple_applications(
    authenticated_client,
    multiple_applications,
):
    url = reverse("application-list")

    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 2


@pytest.mark.django_db
def test_update_application_without_changing_vacancy(
    authenticated_client,
    application,
):
    url = reverse("application-detail", args=[application.id])
    data = {
        "status": Application.Status.APPLIED,
        "source": "Indeed",
        "notes": "Application submitted successfully",
        "applied_at": date.today(),
    }

    response = authenticated_client.patch(
        url,
        data,
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK

    application.refresh_from_db()

    assert application.status == Application.Status.APPLIED
    assert application.source == "Indeed"
    assert application.notes == "Application submitted successfully"
    assert application.applied_at == date.today()

    assert response.data["vacancy"]["id"] == application.vacancy.id


@pytest.mark.django_db
def test_delete_application(
    authenticated_client,
    application,
):
    url = reverse("application-detail", args=[application.id])

    response = authenticated_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Application.objects.filter(id=application.id).exists()
    
