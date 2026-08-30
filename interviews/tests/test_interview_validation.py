import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from interviews.models import Interview


@pytest.mark.django_db
def test_create_interview_with_invalid_type(
    authenticated_client,
    application,
):
    url = reverse("interview-list")

    data = {
        "application_id": application.id,
        "type": "invalid_type",
        "scheduled_at": timezone.now(),
        "result": Interview.Result.PENDING,
    }

    response = authenticated_client.post(
        url,
        data,
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "type" in response.data
    assert Interview.objects.count() == 0


@pytest.mark.django_db
def test_create_interview_with_invalid_result(
    authenticated_client,
    application,
):
    url = reverse("interview-list")

    data = {
        "application_id": application.id,
        "type": Interview.Type.HR,
        "scheduled_at": timezone.now(),
        "result": "invalid_result",
    }

    response = authenticated_client.post(
        url,
        data,
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "result" in response.data
    assert Interview.objects.count() == 0


@pytest.mark.django_db
def test_create_interview_without_required_fields(
    authenticated_client,
):
    response = authenticated_client.post(
        reverse("interview-list"),
        {},
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "application_id" in response.data
    assert "type" in response.data
    assert "scheduled_at" in response.data
    assert not Interview.objects.exists()