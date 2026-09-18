import logging

from rest_framework.viewsets import ModelViewSet
from config.permissions import IsStaffOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from django.db.models.deletion import ProtectedError
from rest_framework import status
from rest_framework.response import Response

from .models import Vacancy
from .schema import vacancy_schema
from .serializers import VacancySerializer


logger = logging.getLogger(__name__)


@vacancy_schema
class VacancyViewSet(ModelViewSet):
    queryset = Vacancy.objects.select_related("company")
    serializer_class = VacancySerializer
    permission_classes = [IsStaffOrReadOnly]
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

    def perform_create(self, serializer):
        vacancy = serializer.save()

        logger.info(
            "Vacancy created: id=%s user_id=%s",
            vacancy.pk,
            self.request.user.pk,
        )

    def destroy(self, request, *args, **kwargs):
        vacancy = self.get_object()
        vacancy_id = vacancy.pk

        try:
            vacancy.delete()
        except ProtectedError:
            return Response(
                {
                    "detail": (
                        "Vacancy cannot be deleted "
                        "because applications exist."
                    )
                },
                status=status.HTTP_409_CONFLICT,
            )

        logger.info(
            "Vacancy deleted: id=%s user_id=%s",
            vacancy_id,
            request.user.pk,
        )

        return Response(status=status.HTTP_204_NO_CONTENT)
