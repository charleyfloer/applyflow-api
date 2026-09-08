import logging

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import Company
from .serializers import CompanySerializer


logger = logging.getLogger(__name__)


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]
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

    def perform_destroy(self, instance):
        company_id = instance.pk
        instance.delete()

        logger.info(
            "Company deleted: id=%s user_id=%s",
            company_id,
            self.request.user.pk,
        )
