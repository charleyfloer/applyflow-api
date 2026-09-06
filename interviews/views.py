from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from applications.models import Application
from .models import Interview
from .serializers import InterviewSerializer


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
