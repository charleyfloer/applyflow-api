import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
def test_refresh_token(api_client, user):
    refresh = RefreshToken.for_user(user)

    url = reverse("token_refresh")

    response = api_client.post(
        url,
        {
            "refresh": str(refresh),
        },
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert response.data["access"]