from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


User = get_user_model()


class NormalizedEmailField(serializers.EmailField):
    def to_internal_value(self, data):
        value = super().to_internal_value(data)
        return value.lower()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
    )
    email = NormalizedEmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    email = NormalizedEmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    class Meta:
        model = User
        fields = ["id", "username", "email"]
        read_only_fields = ["id"]

    