import pytest
from django.urls import reverse
from rest_framework import status

from applications.models import Application


@pytest.mark.django_db
def test_user_cannot_retrieve_another_users_application(
    authenticated_client,
    application,
    another_user,
):
    application.user = another_user
    application.save()

    url = reverse(
        "application-detail",
        args=[application.id],
    )

    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_user_cannot_see_another_users_application_in_list(
    another_authenticated_client,
    application,
):
    response = another_authenticated_client.get(
        reverse("application-list"),
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data == []


@pytest.mark.django_db
def test_user_cannot_update_another_users_application(
    another_authenticated_client,
    application,
):
    url = reverse(
        "application-detail",
        args=[application.id],
    )

    response = another_authenticated_client.patch(
        url,
        {"notes": "Changed by another user"},
        format="json",
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND

    application.refresh_from_db()

    assert application.notes != "Changed by another user"


@pytest.mark.django_db
def test_user_cannot_delete_another_users_application(
    another_authenticated_client,
    application,
):
    url = reverse(
        "application-detail",
        args=[application.id],
    )

    response = another_authenticated_client.delete(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert Application.objects.filter(
        pk=application.pk,
    ).exists()