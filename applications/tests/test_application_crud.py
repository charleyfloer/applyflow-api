import pytest
from django.urls import reverse
from rest_framework import status
from applications.models import Application
from datetime import date


@pytest.mark.django_db
def test_create_application_with_nested_vacancy_representation(
    authenticated_client,
    vacancy,
):
    url = reverse("application-list")

    data = {
        "vacancy_id": vacancy.id,
        "status": "applied",
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

    assert application.status == response.data["status"]
    assert application.vacancy == vacancy

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
    user,
    vacancy,
    vacancy2,
):
    Application.objects.create(
        user=user,
        vacancy=vacancy,
        status="saved",
    )

    Application.objects.create(
            user=user,
            vacancy=vacancy2,
            status="saved",
        )

    url = reverse("application-list")

    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


@pytest.mark.django_db
def test_update_application_with_new_vacancy(
    authenticated_client,
    application,
    vacancy2,
):
    url = reverse("application-detail", args=[application.id])

    data = {
        "vacancy_id": vacancy2.id,
    }

    response = authenticated_client.patch(
        url,
        data,
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK

    application.refresh_from_db()

    assert application.vacancy == vacancy2
    assert response.data["vacancy"]["id"] == vacancy2.id


@pytest.mark.django_db
def test_delete_application(
    authenticated_client,
    application,
):
    url = reverse("application-detail", args=[application.id])

    response = authenticated_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Application.objects.filter(id=application.id).exists()
    
