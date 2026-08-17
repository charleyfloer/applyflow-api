import pytest
from django.urls import reverse
from rest_framework import status
from companies.models import Company


@pytest.mark.django_db
def test_unauthenticated_user_cannot_create_company(api_client):
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