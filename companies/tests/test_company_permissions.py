import pytest
from django.urls import reverse
from rest_framework import status
from companies.models import Company


pytestmark = pytest.mark.django_db


def test_anonymous_user_can_list_companies(api_client, company):
    response = api_client.get(reverse("company-list"))

    assert response.status_code == status.HTTP_200_OK
    assert response.data["results"][0]["id"] == company.pk


def test_anonymous_user_cannot_create_company(api_client):
    url = reverse("company-list")

    data = {
        "name": "Amazon",
        "website": "https://www.amazon.com",
        "location": "Seattle, WA",
    }

    response = api_client.post(
        url,
        data,
        format="json",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert Company.objects.count() == 0


def test_regular_user_cannot_create_company(regular_client):
    response = regular_client.post(
        reverse("company-list"),
        {"name": "Google"},
        format="json",
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Company.objects.count() == 0


def test_regular_user_cannot_delete_company(regular_client, company):
    response = regular_client.delete(
        reverse("company-detail", args=[company.pk]),
    )

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Company.objects.filter(pk=company.pk).exists()