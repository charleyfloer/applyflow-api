from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)

from config.schema import ErrorSerializer, VALIDATION_ERROR_SCHEMA
from .serializers import CompanySerializer


authentication_error = OpenApiResponse(
    response=ErrorSerializer,
    description="Authentication credentials are missing or invalid.",
)
not_found_error = OpenApiResponse(
    response=ErrorSerializer,
    description="Company not found.",
)
validation_error = OpenApiResponse(
    response=VALIDATION_ERROR_SCHEMA,
    description="Validation errors grouped by field name.",
)


company_schema = extend_schema_view(
    list=extend_schema(
        responses={
            200: CompanySerializer(many=True),
            400: validation_error,
            401: authentication_error,
            404: OpenApiResponse(response=ErrorSerializer, description="Invalid page."),
        },
        parameters=[
            OpenApiParameter(
                name="location",
                type=str,
                location=OpenApiParameter.QUERY,
                description="Filter by location (exact match).",
            ),
        ],
    ),
    create=extend_schema(
        responses={
            201: CompanySerializer,
            400: validation_error,
            401: authentication_error,
        },
    ),
    retrieve=extend_schema(
        responses={
            200: CompanySerializer,
            401: authentication_error,
            404: not_found_error,
        },
    ),
    update=extend_schema(
        responses={
            200: CompanySerializer,
            400: validation_error,
            401: authentication_error,
            404: not_found_error,
        },
    ),
    partial_update=extend_schema(
        responses={
            200: CompanySerializer,
            400: validation_error,
            401: authentication_error,
            404: not_found_error,
        },
    ),
    destroy=extend_schema(
        responses={204: None, 401: authentication_error, 404: not_found_error},
    ),
)
