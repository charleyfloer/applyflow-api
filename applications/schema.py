from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)
from config.schema import ErrorSerializer, VALIDATION_ERROR_SCHEMA
from .models import Application
from .serializers import ApplicationSerializer


authentication_error = OpenApiResponse(
    response=ErrorSerializer,
    description="Authentication credentials are missing or invalid.",
)
not_found_error = OpenApiResponse(
    response=ErrorSerializer,
    description="Application not found.",
)
validation_error = OpenApiResponse(
    response=VALIDATION_ERROR_SCHEMA,
    description="Validation errors grouped by field name.",
)
application_validation_error = OpenApiResponse(
    response=VALIDATION_ERROR_SCHEMA,
    description="Validation errors grouped by field name.",
    examples=[
        OpenApiExample(
            "Duplicate application",
            value={
                "vacancy_id": [
                    "You already have an application for this vacancy."
                ],
            },
            response_only=True,
            status_codes=["400"],
        ),
    ],
)


application_schema = extend_schema_view(
    list=extend_schema(
        responses={
            200: ApplicationSerializer(many=True),
            400: validation_error,
            401: authentication_error,
            404: OpenApiResponse(
                response=ErrorSerializer,
                description="Invalid page.",
            ),
        },
        parameters=[
            OpenApiParameter(
                name="status",
                type=str,
                location=OpenApiParameter.QUERY,
                enum=Application.Status.values,
                description="Filter by application status.",
            ),
            OpenApiParameter(
                name="vacancy__title",
                type=str,
                location=OpenApiParameter.QUERY,
                description="Filter by vacancy title (exact match).",
            ),
        ],
    ),
    create=extend_schema(
        responses={
            201: ApplicationSerializer,
            400: application_validation_error,
            401: authentication_error,
        },
    ),
    retrieve=extend_schema(
        responses={
            200: ApplicationSerializer,
            401: authentication_error,
            404: not_found_error,
        },
    ),
    update=extend_schema(
        responses={
            200: ApplicationSerializer,
            400: application_validation_error,
            401: authentication_error,
            404: not_found_error,
        },
    ),
    partial_update=extend_schema(
        responses={
            200: ApplicationSerializer,
            400: application_validation_error,
            401: authentication_error,
            404: not_found_error,
        },
    ),
    destroy=extend_schema(
        responses={
            204: None,
            401: authentication_error,
            404: not_found_error,
        },
    ),
)
