import pytest
from django.urls import reverse
from rest_framework import status


pytestmark = pytest.mark.django_db


def test_dashboard_statistics(
    authenticated_client, 
    multiple_applications,
):
    response = authenticated_client.get(reverse("dashboard"))

    assert response.status_code == status.HTTP_200_OK
    assert response.data["total_applications"] == 4
    assert response.data["by_status"]["applied"] == 3
    assert response.data["by_status"]["interview"] == 1


def test_dashboard_returns_zeros_when_no_applications(
    authenticated_client,
):
    response = authenticated_client.get(
        reverse("dashboard")
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["total_applications"] == 0
    assert response.data["by_status"] == {
        "saved": 0,
        "applied": 0,
        "screening": 0,
        "interview": 0,
        "offer": 0,
        "rejected": 0,
        "withdrawn": 0,
    }


def test_dashboard_only_counts_current_user_application(
    another_authenticated_client,
    application,
    multiple_applications,
):
    response = another_authenticated_client.get(
        reverse("dashboard")
    )

    assert response.status_code == status.HTTP_200_OK

    assert response.data["total_applications"] == 1
    assert response.data["by_status"]["saved"] == 1
    assert response.data["by_status"]["applied"] == 0
    assert response.data["by_status"]["interview"] == 0


def test_dashboard_requires_authentication(
    api_client,
):
    response = api_client.get(
        reverse("dashboard")
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED