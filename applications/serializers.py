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

        queryset = Application.objects.filter(
            user=user,
            vacancy=vacancy,
        )

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                "You already have an application for this vacancy."
            )

        return attrs