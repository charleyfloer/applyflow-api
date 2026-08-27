from rest_framework import serializers

from applications.models import Application
from vacancies.models import Vacancy
from vacancies.serializers import VacancySerializer


class ApplicationSerializer(serializers.ModelSerializer):
    vacancy = VacancySerializer(read_only=True)

    vacancy_id = serializers.PrimaryKeyRelatedField(
        queryset=Vacancy.objects.all(),
        source="vacancy",
        write_only=True,
    )

    class Meta:
        model = Application
        fields = (
            "id",
            "user",
            "vacancy",
            "vacancy_id",
            "status",
            "source",
            "resume",
            "cover_letter",
            "notes",
            "applied_at",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "user",
            "created_at",
            "updated_at",
        )

    def validate(self, attrs):
        user = self.context["request"].user

        vacancy = attrs.get(
            "vacancy",
            getattr(self.instance, "vacancy", None),
        )
        status = attrs.get(
            "status",
            getattr(self.instance, "status", Application.Status.SAVED),
        )
        applied_at = attrs.get(
            "applied_at",
            getattr(self.instance, "applied_at", None),
        )

        queryset = Application.objects.filter(
            user=user,
            vacancy=vacancy,
        )

        if self.instance is not None:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError({
                "vacancy_id": (
                    "You already have an application for this vacancy."
                ),
            })

        applied_statuses = {
            Application.Status.APPLIED,
            Application.Status.SCREENING,
            Application.Status.INTERVIEW,
            Application.Status.OFFER,
            Application.Status.REJECTED,
            Application.Status.WITHDRAWN,
        }

        if status == Application.Status.SAVED and applied_at is not None:
            raise serializers.ValidationError({
                "applied_at": (
                    "A saved application cannot have an application date."
                ),
            })

        if status in applied_statuses and applied_at is None:
            raise serializers.ValidationError({
                "applied_at": (
                    "Application date is required for this status."
                ),
            })

        return attrs