import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from interviews.models import Interview


@pytest.mark.django_db
def test_user_cannot_retrieve_another_users_interview(
    another_authenticated_client,
    interview,
):
    url = reverse(
        "interview-detail",
        args=[interview.id],
    )

    response = another_authenticated_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_user_sees_only_own_interviews(
    authenticated_client,
    interview,
    another_interview,
):
    response = authenticated_client.get(
        reverse("interview-list"),
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["id"] == interview.id


@pytest.mark.django_db
def test_user_cannot_create_interview_for_another_users_application(
    another_authenticated_client,
    application,
):
    data = {
        "application_id": application.id,
        "type": Interview.Type.HR,
        "scheduled_at": timezone.now(),
        "result": Interview.Result.PENDING,
    }

    response = another_authenticated_client.post(
        reverse("interview-list"),
        data,
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "application_id" in response.data
    assert not Interview.objects.exists()


@pytest.mark.django_db
def test_user_cannot_update_another_users_interview(
    another_authenticated_client,
    interview,
):
    url = reverse(
        "interview-detail",
        args=[interview.id],
    )

    response = another_authenticated_client.patch(
        url,
        {"notes": "Changed by another user"},
        format="json",
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

    interview.refresh_from_db()

    assert interview.notes != "Changed by another user"


@pytest.mark.django_db
def test_user_cannot_delete_another_users_interview(
    another_authenticated_client,
    interview,
):
    url = reverse(
        "interview-detail",
        args=[interview.id],
    )

    response = another_authenticated_client.delete(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert Interview.objects.filter(
        pk=interview.pk,
    ).exists()