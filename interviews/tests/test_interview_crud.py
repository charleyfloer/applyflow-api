import pytest
from django.utils import timezone
from django.urls import reverse
from rest_framework import status

from interviews.models import Interview


@pytest.mark.django_db
def test_create_interview_with_nested_application_representation(
    authenticated_client,
    application,
    user,
    vacancy,
):
    url = reverse("interview-list")

    data = {
        "application_id": application.id,
        "type": Interview.Type.HR,
        "scheduled_at": timezone.now(),
        "result": Interview.Result.PASSED,
    }

    response = authenticated_client.post(
        url,
        data,
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert Interview.objects.count() == 1

    interview = Interview.objects.get(pk=response.data["id"])

    assert interview.application.user == user
    assert interview.application.vacancy == vacancy
    assert interview.type == Interview.Type.HR
    assert "scheduled_at" in response.data
    assert interview.result == Interview.Result.PASSED
    
    assert response.data["application"]["id"] == application.id
    assert response.data["application"]["status"] == application.status


@pytest.mark.django_db
def test_retrieve_interview_with_nested_application(
    authenticated_client,
    interview,
):
    url = reverse("interview-detail", args=[interview.id])

    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    assert response.data["id"] == interview.id
    assert response.data["type"] == interview.type
    assert response.data["result"] == interview.result

    assert response.data["application"]["id"] == interview.application.id
    assert response.data["application"]["status"] == interview.application.status


@pytest.mark.django_db
def test_list_multiple_interviews(
    authenticated_client,
    application,
):
    Interview.objects.create(
        application=application,
        type=Interview.Type.HR,
        scheduled_at=timezone.now(),
    )
    Interview.objects.create(
        application=application,
        type=Interview.Type.TECHNICAL,
        scheduled_at=timezone.now(),
    )

    response = authenticated_client.get(reverse("interview-list"))

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) == 2


@pytest.mark.django_db
def test_update_interview_without_changing_application(
    authenticated_client,
    interview,
):
    url = reverse("interview-detail", args=[interview.id])
    data = {
        "type": Interview.Type.TECHNICAL,
        "result": Interview.Result.PASSED,
        "notes": "Technical interview completed successfully",
    }

    response = authenticated_client.patch(
        url,
        data,
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK

    interview.refresh_from_db()

    assert interview.type == Interview.Type.TECHNICAL
    assert interview.result == Interview.Result.PASSED
    assert interview.notes == "Technical interview completed successfully"
    assert response.data["application"]["id"] == interview.application.id


@pytest.mark.django_db
def test_delete_interview(
    authenticated_client,
    interview,
):
    url = reverse("interview-detail", args=[interview.id])

    response = authenticated_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Interview.objects.filter(id=interview.id).exists()
