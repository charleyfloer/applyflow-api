import logging

from rest_framework.viewsets import ModelViewSet
from config.permissions import IsStaffOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from django.db.models.deletion import ProtectedError
from rest_framework import status
from rest_framework.response import Response

from .models import Company
from .schema import company_schema
from .serializers import CompanySerializer


logger = logging.getLogger(__name__)


@company_schema
class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsStaffOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["location"]
    search_fields = ["name", "website", "location"]
    ordering_fields = ["name", "location", "created_at", "updated_at"]
    ordering = ["-created_at", "-id"]

    def perform_create(self, serializer):
        company = serializer.save()

        logger.info(
            "Company created: id=%s user_id=%s",
            company.pk,
            self.request.user.pk,
        )

    def destroy(self, request, *args, **kwargs):
        company = self.get_object()
        company_id = company.pk

        try:
            company.delete()
        except ProtectedError:
            return Response(
                {
                    "detail": (
                        "Company cannot be deleted "
                        "because vacancies exist."
                    )
                },
                status=status.HTTP_409_CONFLICT,
            )

        logger.info(
            "Company deleted: id=%s user_id=%s",
            company_id,
            request.user.pk,
        )

        return Response(status=status.HTTP_204_NO_CONTENT)
