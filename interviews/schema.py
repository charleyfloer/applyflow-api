from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)

from config.schema import ErrorSerializer, VALIDATION_ERROR_SCHEMA
from .models import Interview
from .serializers import InterviewSerializer


authentication_error = OpenApiResponse(
    response=ErrorSerializer,
    description="Authentication credentials are missing or invalid.",
)
not_found_error = OpenApiResponse(
    response=ErrorSerializer,
    description="Interview not found.",
)
validation_error = OpenApiResponse(
    response=VALIDATION_ERROR_SCHEMA,
    description="Validation errors grouped by field name.",
)

interview_schema = extend_schema_view(
    list=extend_schema(
        responses={
            200: InterviewSerializer(many=True),
            400: validation_error,
            401: authentication_error,
            404: OpenApiResponse(response=ErrorSerializer, description="Invalid page."),
        },
        parameters=[
            OpenApiParameter(
                name="type",
                type=str,
                location=OpenApiParameter.QUERY,
                enum=Interview.Type.values,
                description="Filter by interview type.",
            ),
            OpenApiParameter(
                name="result",
                type=str,
                location=OpenApiParameter.QUERY,
                enum=Interview.Result.values,
                description="Filter by interview result.",
            ),
        ],
    ),
    create=extend_schema(
        responses={
            201: InterviewSerializer,
            400: validation_error,
            401: authentication_error,
        },
    ),
    retrieve=extend_schema(
        responses={
            200: InterviewSerializer,
            401: authentication_error,
            404: not_found_error,
        },
    ),
    update=extend_schema(
        responses={
            200: InterviewSerializer,
            400: validation_error,
            401: authentication_error,
            404: not_found_error,
        },
    ),
    partial_update=extend_schema(
        responses={
            200: InterviewSerializer,
            400: validation_error,
            401: authentication_error,
            404: not_found_error,
        },
    ),
    destroy=extend_schema(
        responses={204: None, 401: authentication_error, 404: not_found_error},
    ),
)
