from rest_framework import serializers
from .models import Vacancy

from companies.models import Company
from companies.serializers import CompanySerializer


class VacancySerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)

    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(),
        source="company",
        write_only=True,
    )

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
            "company",
            "company_id",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_salary_min(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError(
                "Minimum salary cannot be negative."
            )
                        
        return value

    def validate_salary_max(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError(
                "Maximum salary cannot be negative."
            )
                            
        return value

    def validate(self, attrs):
        salary_min = attrs.get(
            "salary_min",
            getattr(self.instance, "salary_min", None),
        )

        salary_max = attrs.get(
            "salary_max",
            getattr(self.instance, "salary_max", None),
        )

        if (
            salary_min is not None
            and salary_max is not None
            and salary_min > salary_max
        ):
            raise serializers.ValidationError(
                "Minimum salary cannot be greater than maximum salary."
            )

        return attrs