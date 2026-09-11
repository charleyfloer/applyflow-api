from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)

from config.schema import ErrorSerializer, VALIDATION_ERROR_SCHEMA
from .serializers import RegisterSerializer, UserSerializer


class TokenErrorSerializer(ErrorSerializer):
    code = serializers.CharField(required=False)


authentication_error = OpenApiResponse(
    response=ErrorSerializer,
    description="Authentication credentials are missing or invalid.",
)
validation_error = OpenApiResponse(
    response=VALIDATION_ERROR_SCHEMA,
    description="Validation errors grouped by field name.",
)

register_schema = extend_schema_view(
    post=extend_schema(
        responses={
            201: RegisterSerializer,
            400: validation_error,
            401: OpenApiResponse(
                response=ErrorSerializer,
                description=(
                    "The provided authentication token is invalid or expired. "
                    "Registration does not require authentication. "
                    "Remove the Authorization header and try again."
                ),
            ),
        },
    ),
)
profile_schema = extend_schema_view(
    get=extend_schema(responses={200: UserSerializer, 401: authentication_error}),
    put=extend_schema(
        responses={200: UserSerializer, 400: validation_error, 401: authentication_error},
    ),
    patch=extend_schema(
        responses={200: UserSerializer, 400: validation_error, 401: authentication_error},
    ),
)
login_schema = extend_schema_view(
    post=extend_schema(
        responses={
            200: TokenObtainPairSerializer,
            400: validation_error,
            401: OpenApiResponse(
                response=ErrorSerializer,
                description="No active account found with the given credentials.",
            ),
        },
    ),
)
token_refresh_schema = extend_schema_view(
    post=extend_schema(
        responses={
            200: TokenRefreshSerializer,
            400: validation_error,
            401: OpenApiResponse(
                response=TokenErrorSerializer,
                description="Refresh token is invalid or expired, or the user is inactive.",
            ),
        },
    ),
)
