import logging
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from applications.models import Application
from applications.schema import application_schema
from applications.serializers import ApplicationSerializer


logger = logging.getLogger(__name__)


@application_schema
class ApplicationViewSet(ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["status", "vacancy__title"]
    search_fields = ["notes", "source", "vacancy__title"]
    ordering_fields = ["status", "applied_at", "created_at", "updated_at"]
    ordering = ["-created_at", "-id"]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Application.objects.none()

        return (
            Application.objects
            .filter(user=self.request.user)
            .select_related("vacancy", "vacancy__company")
        )

    def perform_create(self, serializer):
        application = serializer.save(user=self.request.user)

        logger.info(
            "Application created: id=%s user_id=%s",
            application.id,
            self.request.user.id,
        )

    def perform_update(self, serializer):
        old_status = serializer.instance.status
        application = serializer.save()

        if old_status != application.status:
            logger.info(
                "Application status changed: id=%s user_id=%s "
                "old_status=%s new_status=%s",
                application.pk,
                self.request.user.pk,
                old_status,
                application.status,
            )
    
    def perform_destroy(self, instance):
        application_id = instance.pk
        instance.delete()

        logger.info(
            "Application deleted: id=%s user_id=%s",
            application_id,
            self.request.user.pk,
        )
