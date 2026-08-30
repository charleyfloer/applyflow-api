import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from interviews.models import Interview


@pytest.mark.django_db
def test_unauthenticated_user_cannot_create_interview(
    api_client,
    application,
):
    url = reverse("interview-list")

    data = {
        "application_id": application.id,
        "type": Interview.Type.HR,
        "scheduled_at": timezone.now(),
    }

    response = api_client.post(
        url,
        data,
        format="json",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert Interview.objects.count() == 0
