import pytest
from django.urls import reverse
from rest_framework import status

from applications.models import Application


@pytest.mark.django_db
def test_unauthenticated_user_cannot_create_application(
    api_client,
    vacancy,
):
    url = reverse("application-list")

    data = {
        "vacancy_id": vacancy.id,
        "status": "saved"
    }

    response = api_client.post(
        url,
        data,
        format="json",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert Application.objects.count() == 0