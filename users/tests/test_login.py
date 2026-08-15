import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_login_returns_tokens(api_client, user):
    url = reverse("login")

    data = {
        "username": "andrew",
        "password": "Testuser123!",
    }

    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data