import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_filter_companies_by_location(
    authenticated_client,
    multiple_companies,
):
    response = authenticated_client.get(
        reverse("company-list"),
        {"location": "California"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 2
    assert all(
        company["location"] == "California"
        for company in response.data["results"]
    )


@pytest.mark.django_db
def test_search_companies_by_name(
    authenticated_client,
    multiple_companies,
):
    response = authenticated_client.get(
        reverse("company-list"),
        {"search": "micro"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert response.data["results"][0]["name"] == "Microsoft"


@pytest.mark.django_db
def test_order_companies_by_name(
    authenticated_client,
    multiple_companies,
):
    response = authenticated_client.get(
        reverse("company-list"),
        {"ordering": "name"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert [
        company["name"]
        for company in response.data["results"]
    ] == ["Amazon", "Apple"]


@pytest.mark.django_db
def test_companies_pagination(
    authenticated_client,
    multiple_companies,
):
    url = reverse("company-list")

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
