import pytest
from django.urls import reverse
from rest_framework import status

from vacancies.models import EmploymentType


@pytest.mark.django_db
def test_filter_and_order_vacancies(
    authenticated_client,
    multiple_vacancies,
):
    response = authenticated_client.get(
        reverse("vacancy-list"),
        {
            "employment_type": EmploymentType.FULL_TIME,
            "ordering": "-salary_max",
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 3
    assert [
        vacancy["title"]
        for vacancy in response.data["results"]
    ] == [
        "Senior Python Developer",
        "Frontend Developer",
    ]
    assert all(
        vacancy["employment_type"] == EmploymentType.FULL_TIME
        for vacancy in response.data["results"]
    )


@pytest.mark.django_db
def test_search_vacancies_by_description(
    authenticated_client,
    multiple_vacancies,
):
    response = authenticated_client.get(
        reverse("vacancy-list"),
        {"search": "React"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert response.data["results"][0]["title"] == "Frontend Developer"
    assert response.data["results"][0]["description"] == (
        "Development of React user interfaces"
    )


@pytest.mark.django_db
def test_vacancies_pagination(
    authenticated_client,
    multiple_vacancies,
):
    url = reverse("vacancy-list")

    first_page = authenticated_client.get(url, {"page": 1})

    assert first_page.status_code == status.HTTP_200_OK
    assert first_page.data["count"] == 4
    assert len(first_page.data["results"]) == 2
    assert first_page.data["previous"] is None
    assert first_page.data["next"] is not None

    second_page = authenticated_client.get(url, {"page": 2})

    assert second_page.status_code == status.HTTP_200_OK
    assert second_page.data["count"] == 4
    assert len(second_page.data["results"]) == 2
    assert second_page.data["previous"] is not None
    assert second_page.data["next"] is None
