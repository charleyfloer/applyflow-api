import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

pytestmark = pytest.mark.django_db

User = get_user_model()


def test_protected_endpoint_without_token(api_client):
    url = reverse("profile")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_update_user_profile_with_patch(api_client, user, access_token):
    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {access_token}"
    )

    url = reverse("profile")

    data = {
        "username": "updated_user",
        "email": "updated@example.com",
    }

    response = api_client.patch(
        url,
        data,
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK

    assert response.data["username"] == "updated_user"
    assert response.data["email"] == "updated@example.com"

    user.refresh_from_db()

    assert user.username == "updated_user"
    assert user.email == "updated@example.com"


def test_partial_update_user_profile_with_another_users_email_in_uppercase(
    api_client, 
    user, 
    user2, 
    access_token
):
    original_email = user.email
    original_username = user.username

    api_client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {access_token}"
    )

    url = reverse("profile")

    data = {
        "username": "updated_user",
        "email": user2.email.upper(),
    }

    response = api_client.patch(
        url,
        data,
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "email" in response.data

    user.refresh_from_db()

    assert user.email == original_email
    assert user.username == original_username
