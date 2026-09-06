import pytest
from django.urls import reverse
from rest_framework import status

from applications.models import Application


@pytest.mark.django_db
def test_filter_search_and_order_applications(
    authenticated_client,
    multiple_applications,
    vacancy,
    vacancy2,
):
    response = authenticated_client.get(
        reverse("application-list"),
        {
            "status": Application.Status.APPLIED,
            "search": "develop",
            "ordering": "-applied_at",  
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 2
    assert len(response.data["results"]) == 2

    assert response.data["results"][0]["status"] == Application.Status.APPLIED
    assert response.data["results"][0]["vacancy"]["id"] == vacancy.id
    assert response.data["results"][0]["vacancy"]["title"] == vacancy.title

    assert response.data["results"][1]["status"] == Application.Status.APPLIED
    assert response.data["results"][1]["vacancy"]["id"] == vacancy2.id
    assert response.data["results"][1]["vacancy"]["title"] == vacancy2.title


@pytest.mark.django_db
def test_applications_pagination(
    authenticated_client,
    multiple_applications,
):
    url = reverse("application-list")

    first_page = authenticated_client.get(url, {"page": 1})

    assert first_page.status_code == status.HTTP_200_OK
    assert first_page.data["count"] == 4
    assert len(first_page.data["results"]) == 2
    assert first_page.data["previous"] is None
    assert first_page.data["next"] is not None

    second_page = authenticated_client.get(url, {"page": 2})

    assert second_page.status_code == status.HTTP_200_OK
    assert len(second_page.data["results"]) == 2
    assert second_page.data["previous"] is not None
    assert second_page.data["next"] is None