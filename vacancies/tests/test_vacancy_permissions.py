import pytest
from django.urls import reverse
from rest_framework import status

from vacancies.models import Vacancy


@pytest.mark.django_db
def test_unauthenticated_user_cannot_create_vacancy(
    api_client,
    company,
):
    url = reverse("vacancy-list")

    data = {
        "company_id": company.id,
        "title": "Python Developer",
        "description": "Backend development",
        "website": "https://example.com/jobs/python",
        "location": "Remote",
        "employment_type": "full_time",
        "salary_min": "100000.00",
        "salary_max": "150000.00",
    }

    response = api_client.post(
        url,
        data,
        format="json",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert Vacancy.objects.count() == 0