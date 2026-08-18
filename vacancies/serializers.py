from rest_framework import serializers
from .models import Vacancy


class VacancySerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacancy
        fields = [
            "id",
            "company",
            "title",
            "description",
            "website",
            "location",
            "employment_type",
            "salary_min",
            "salary_max",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
