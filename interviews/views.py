from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from applications.models import Application

from .models import Interview
from .serializers import InterviewSerializer


class InterviewViewSet(ModelViewSet):
    serializer_class = InterviewSerializer
    permission_classes = [IsAuthenticated]

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
        serializer.fields["application_id"].queryset = (
            Application.objects.filter(user=self.request.user)
        )
        return serializer


