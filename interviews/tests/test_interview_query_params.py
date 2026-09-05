import pytest
from django.urls import reverse
from rest_framework import status

from interviews.models import Interview


@pytest.mark.django_db
def test_filter_and_order_interviews(
    authenticated_client,
    multiple_interviews,
):
    response = authenticated_client.get(
        reverse("interview-list"),
        {
            "result": Interview.Result.PASSED,
            "ordering": "-scheduled_at",
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 2
    assert [
        interview["notes"]
        for interview in response.data["results"]
    ] == [
        "Django technical interview completed",
        "HR interview completed",
    ]
    assert all(
        interview["result"] == Interview.Result.PASSED
        for interview in response.data["results"]
    )


@pytest.mark.django_db
def test_search_interviews_by_vacancy_title(
    authenticated_client,
    multiple_interviews,
):
    response = authenticated_client.get(
        reverse("interview-list"),
        {"search": "Frontend"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert response.data["results"][0]["application"]["vacancy"]["title"] == (
        "Frontend Developer"
    )


@pytest.mark.django_db
def test_interviews_pagination(
    authenticated_client,
    multiple_interviews,
):
    url = reverse("interview-list")

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
