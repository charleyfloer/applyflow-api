from rest_framework import serializers

from applications.models import Application
from applications.serializers import ApplicationSerializer

from .models import Interview


class InterviewSerializer(serializers.ModelSerializer):
    application = ApplicationSerializer(read_only=True)

    application_id = serializers.PrimaryKeyRelatedField(
        queryset=Application.objects.all(),
        source="application",
        write_only=True,
    )

    class Meta:
        model = Interview
        fields = (
            "id",
            "application",
            "application_id",
            "type",
            "scheduled_at",
            "result",
            "notes",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )
