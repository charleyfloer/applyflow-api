from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from applications.models import Application
from applications.serializers import ApplicationSerializer


class ApplicationViewSet(ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Application.objects
            .filter(user=self.request.user)
            .select_related("vacancy", "vacancy__company")
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
