import logging
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from applications.models import Application
from .models import Interview
from .serializers import InterviewSerializer


logger = logging.getLogger(__name__)


class InterviewViewSet(ModelViewSet):
    serializer_class = InterviewSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["type", "result"]
    search_fields = [
        "notes",
        "application__vacancy__title",
        "application__vacancy__company__name",
    ]
    ordering_fields = ["scheduled_at", "created_at", "updated_at"]
    ordering = ["scheduled_at", "id"]

    def get_queryset(self):
        return (
            Interview.objects
            .filter(application__user=self.request.user)
            .select_related(
                "application",
                "application__vacancy",
                "application__vacancy__company",
            )
        )

    def get_serializer(self, *args, **kwargs):
        serializer = super().get_serializer(*args, **kwargs)
        interview_serializer = getattr(serializer, "child", serializer)
        interview_serializer.fields["application_id"].queryset = (
            Application.objects.filter(user=self.request.user)
        )
        return serializer

    def perform_create(self, serializer):
        interview = serializer.save()
    
        logger.info(
            "Interview created: id=%s application_id=%s",
            interview.id,
            interview.application_id,
        )

    def perform_update(self, serializer):
        old_result = serializer.instance.result
        old_scheduled_at = serializer.instance.scheduled_at
        interview = serializer.save()
    
        if old_result != interview.result:
            logger.info(
                "Interview result changed: id=%s user_id=%s "
                "old_result=%s new_result=%s",
                interview.pk,
                self.request.user.pk,
                old_result,
                interview.result,
            )

        if old_scheduled_at != interview.scheduled_at:
            logger.info(
                "Interview date changed: id=%s user_id=%s "
                "old_date=%s new_date=%s",
                interview.pk,
                self.request.user.pk,
                old_scheduled_at,
                interview.scheduled_at,
            )
        
    def perform_destroy(self, instance):
        interview_id = instance.pk
        instance.delete()
        
        logger.info(
            "Interview deleted: id=%s user_id=%s",
            interview_id,
            self.request.user.pk,
        )
