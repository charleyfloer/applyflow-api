import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_update_company_with_too_short_name(
    authenticated_client,
    company,
):
    url = reverse("company-detail", args=[company.id])

    response = authenticated_client.patch(
        url,
        {"name": "J"},
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "name" in response.data
    assert (
        str(response.data["name"][0])
        == "Company name must contain at least 2 characters."
    )

    company.refresh_from_db()
    assert company.name == "Google"


@pytest.mark.django_db
def test_update_company_with_invalid_website(
    authenticated_client,
    company,
):
    url = reverse("company-detail", args=[company.id])

    response = authenticated_client.patch(
        url,
        {"website": "invalid-url"},
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "website" in response.data

    company.refresh_from_db()
    assert company.website == "https://google.com"