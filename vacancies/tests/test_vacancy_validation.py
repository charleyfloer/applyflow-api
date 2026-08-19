import pytest
from django.urls import reverse
from rest_framework import status

from vacancies.models import Vacancy


@pytest.mark.django_db
def test_create_vacancy_with_invalid_employment_type(
    authenticated_client,
    company,
):
    url = reverse("vacancy-list")

    data = {
        "company_id": company.id,
        "title": "Python Developer",
        "description": "Backend development",
        "website": "https://example.com/jobs/python",
        "location": "Remote",
        "employment_type": "freelance",
        "salary_min": "100000.00",
        "salary_max": "150000.00",
    }

    response = authenticated_client.post(
        url,
        data,
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "employment_type" in response.data
    assert Vacancy.objects.count() == 0


@pytest.mark.django_db
def test_create_vacancy_with_both_negative_salaries(
    authenticated_client,
    company,
):
    response = authenticated_client.post(
        reverse("vacancy-list"),
        {
            "company_id": company.id,
            "title": "Python Developer",
            "description": "Backend development",
            "employment_type": "full_time",
            "salary_min": "-100000.00",
            "salary_max": "-50000.00",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "salary_min" in response.data
    assert "salary_max" in response.data
    assert Vacancy.objects.count() == 0


@pytest.mark.django_db
def test_partial_update_rejects_salary_max_less_than_existing_salary_min(
    authenticated_client,
    vacancy,
):
    url = reverse("vacancy-detail", args=[vacancy.id])

    response = authenticated_client.patch(
        url,
        {
            "salary_max": "50000.00",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "non_field_errors" in response.data
    assert str(response.data["non_field_errors"][0]) == (
        "Minimum salary cannot be greater than maximum salary."
    )

    vacancy.refresh_from_db()

    assert vacancy.salary_min == 100000
    assert vacancy.salary_max == 150000


@pytest.mark.django_db
def test_cannot_create_vacancy_with_nonexistent_company(
    authenticated_client,
):
    url = reverse("vacancy-list")

    nonexistent_company_id = 999999

    data = {
        "company_id": nonexistent_company_id,
        "title": "Python Developer",
        "description": "Backend development",
        "website": "https://example.com/jobs/python",
        "location": "Remote",
        "employment_type": "full_time",
        "salary_min": "100000.00",
        "salary_max": "150000.00",
    }

    response = authenticated_client.post(
        url,
        data,
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "company_id" in response.data
    assert Vacancy.objects.count() == 0