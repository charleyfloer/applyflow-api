import pytest
from django.urls import reverse
from rest_framework import status
from vacancies.models import Vacancy


@pytest.mark.django_db
def test_create_vacancy_with_nested_company_representation(
    authenticated_client,
    company,
):
    url = reverse("vacancy-list")

    data = {
        "company_id": company.id,
        "title": "Django Developer",
        "description": "Develop REST APIs",
        "website": "https://linkedin.com/jobs/django",
        "location": "New York",
        "employment_type": "full_time",
        "salary_min": "90000.00",
        "salary_max": "130000.00",
    }

    response = authenticated_client.post(
        url,
        data,
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert Vacancy.objects.count() == 1

    vacancy = Vacancy.objects.get(pk=response.data["id"])

    assert vacancy.title == "Django Developer"
    assert vacancy.company == company

    assert response.data["company"]["id"] == company.id
    assert response.data["company"]["name"] == company.name
    assert response.data["company"]["website"] == company.website


@pytest.mark.django_db
def test_retrieve_vacancy_with_nested_company(
    authenticated_client,
    vacancy,
):
    url = reverse("vacancy-detail", args=[vacancy.id])

    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    assert response.data["id"] == vacancy.id
    assert response.data["title"] == vacancy.title

    assert response.data["company"]["id"] == vacancy.company.id
    assert response.data["company"]["name"] == vacancy.company.name
    assert response.data["company"]["website"] == vacancy.company.website


@pytest.mark.django_db
def test_list_multiple_vacancies(
    authenticated_client,
    company,
):
    Vacancy.objects.create(
        company=company,
        title="Python Developer",
        description="Python backend development",
    )

    Vacancy.objects.create(
        company=company,
        title="Django Developer",
        description="Django REST API development",
    )

    url = reverse("vacancy-list")

    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


@pytest.mark.django_db
def test_update_vacancy_with_new_company(
    authenticated_client,
    vacancy,
    another_company,
):
    url = reverse("vacancy-detail", args=[vacancy.id])

    data = {
            "company_id": another_company.id,
            "title": "Senior Python Developer",
            "description": "Updated description",
            "website": "https://example.com/django/djangorest/",
            "location": "Miami",
            "employment_type": "full_time",
            "salary_min": "150000.00",
            "salary_max": "200000.00",
        }

    response = authenticated_client.put(
        url,
        data,
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK

    vacancy.refresh_from_db()

    assert vacancy.title == "Senior Python Developer"
    assert vacancy.company == another_company

    assert response.data["company"]["id"] == another_company.id
    assert response.data["company"]["name"] == another_company.name


@pytest.mark.django_db
def test_delete_vacancy(
    authenticated_client,
    vacancy,
):
    url = reverse("vacancy-detail", args=[vacancy.id])

    response = authenticated_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Vacancy.objects.filter(id=vacancy.id).exists()
