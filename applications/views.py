from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from applications.models import Application
from applications.serializers import ApplicationSerializer


class ApplicationViewSet(ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["status", "vacancy__title"]
    search_fields = ["notes", "source", "vacancy__title"]
    ordering_fields = ["status", "applied_at", "created_at", "updated_at"]
    ordering = ["-created_at", "-id"]

    def get_queryset(self):
        return (
            Application.objects
            .filter(user=self.request.user)
            .select_related("vacancy", "vacancy__company")
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
