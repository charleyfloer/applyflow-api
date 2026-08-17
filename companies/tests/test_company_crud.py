import pytest
from django.urls import reverse
from rest_framework import status
from companies.models import Company


@pytest.mark.django_db
def test_company_list(authenticated_client, company):
    url = reverse("company-list")

    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["id"] == company.id
    assert response.data[0]["name"] == "Google"
    assert response.data[0]["website"] == "https://google.com"
    assert response.data[0]["location"] == "Mountain View, CA"


@pytest.mark.django_db
def test_company_retrieve(authenticated_client, company):
    url = reverse("company-detail", args=[company.id])

    response = authenticated_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == company.id
    assert response.data["name"] == "Google"
    assert response.data["website"] == "https://google.com"
    assert response.data["location"] == "Mountain View, CA"


@pytest.mark.django_db
def test_company_create(authenticated_client):
    url = reverse("company-list")

    data = {
        "name": "Microsoft",
        "website": "https://microsoft.com",
        "location": "Redmond, WA",
    }

    response = authenticated_client.post(
        url,
        data,
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert Company.objects.count() == 1

    company = Company.objects.get(id=response.data["id"])

    assert company.name == "Microsoft"
    assert company.website == "https://microsoft.com"
    assert company.location == "Redmond, WA"


@pytest.mark.django_db
def test_company_update(authenticated_client, company):
    url = reverse("company-detail", args=[company.id])

    data = {
        "name": "Google LLC",
        "website": "https://about.google",
        "location": "California",
    }

    response = authenticated_client.put(
        url,
        data,
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK

    company.refresh_from_db()

    assert company.name == "Google LLC"
    assert company.website == "https://about.google"
    assert company.location == "California"


@pytest.mark.django_db
def test_company_partial_update(authenticated_client, company):
    url = reverse("company-detail", args=[company.id])

    response = authenticated_client.patch(
        url,
        {
            "location": "New York",
        },
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK

    company.refresh_from_db()

    assert company.location == "New York"
    assert company.name == "Google"
    assert company.website == "https://google.com"


@pytest.mark.django_db
def test_company_delete(authenticated_client, company):
    url = reverse("company-detail", args=[company.id])

    response = authenticated_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Company.objects.filter(id=company.id).exists()