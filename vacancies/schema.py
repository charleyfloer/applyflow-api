from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)

from config.schema import ErrorSerializer, VALIDATION_ERROR_SCHEMA
from .models import EmploymentType
from .serializers import VacancySerializer


authentication_error = OpenApiResponse(
    response=ErrorSerializer,
    description="Authentication credentials are missing or invalid.",
)
not_found_error = OpenApiResponse(
    response=ErrorSerializer,
    description="Vacancy not found.",
)
validation_error = OpenApiResponse(
    response=VALIDATION_ERROR_SCHEMA,
    description="Validation errors grouped by field name.",
)

permission_error = OpenApiResponse(
    response=ErrorSerializer,
    description="Only staff users can modify vacancies.",
)
conflict_error = OpenApiResponse(
    response=ErrorSerializer,
    description="Vacancy cannot be deleted because applications exist.",
)

vacancy_schema = extend_schema_view(
    list=extend_schema(
        responses={
            200: VacancySerializer(many=True),
            400: validation_error,
            401: authentication_error,
            404: OpenApiResponse(response=ErrorSerializer, description="Invalid page."),
        },
        parameters=[
            OpenApiParameter(
                name="company",
                type=int,
                location=OpenApiParameter.QUERY,
                description="Filter by company ID.",
            ),
            OpenApiParameter(
                name="employment_type",
                type=str,
                location=OpenApiParameter.QUERY,
                enum=EmploymentType.values,
                description="Filter by employment type.",
            ),
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
            201: VacancySerializer,
            400: validation_error,
            401: authentication_error,
            403: permission_error,
        },
    ),
    retrieve=extend_schema(
        responses={
            200: VacancySerializer,
            401: authentication_error,
            404: not_found_error,
        },
    ),
    update=extend_schema(
        responses={
            200: VacancySerializer,
            400: validation_error,
            401: authentication_error,
            403: permission_error,
            404: not_found_error,
        },
    ),
    partial_update=extend_schema(
        responses={
            200: VacancySerializer,
            400: validation_error,
            401: authentication_error,
            403: permission_error,
            404: not_found_error,
        },
    ),
    destroy=extend_schema(
        responses={
            204: None,
            401: authentication_error,
            403: permission_error,
            404: not_found_error,
            409: conflict_error,
        },
    ),
)
