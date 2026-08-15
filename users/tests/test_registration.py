import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

pytestmark = pytest.mark.django_db

User = get_user_model()


def test_register_user(api_client):
    url = reverse("register")

    data = {
        "username": "john",
        "email": "white@gmail.com",
        "password": "Mrcrow123!",
    }

    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.count() == 1

    user = User.objects.get(username="john")

    assert user.email == "white@gmail.com"
    assert user.check_password("Mrcrow123!")


def test_register_user_with_duplicate_email(api_client, user):
    response = api_client.post(
        reverse("register"),
        {
            "username": "Nick",
            "email": "andrew@gmail.com",
            "password": "Seconduser123!",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert User.objects.count() == 1


def test_register_user_with_invalid_password(api_client):
    url = reverse("register")

    data = {
        "username": "test_user",
        "email": "black@gmail.com",
        "password": "/#$%",
    }

    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert User.objects.count() == 0