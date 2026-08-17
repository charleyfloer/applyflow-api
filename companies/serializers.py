from rest_framework import serializers
from .models import Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "name", "website", "location", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_name(self, value):
            if len(value.strip()) < 2:
                raise serializers.ValidationError(
                    "Company name must contain at least 2 characters."
                )
            
            return value