from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import Vacancy
from .serializers import VacancySerializer


class VacancyViewSet(ModelViewSet):
    queryset = Vacancy.objects.select_related("company")
    serializer_class = VacancySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["company", "employment_type", "location"]
    search_fields = ["title", "description", "location", "company__name"]
    ordering_fields = [
        "title",
        "salary_min",
        "salary_max",
        "created_at",
        "updated_at",
    ]
    ordering = ["-created_at", "-id"]
