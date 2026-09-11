from drf_spectacular.utils import OpenApiResponse, extend_schema

from config.schema import ErrorSerializer
from .serializers import DashboardSerializer


dashboard_schema = extend_schema(
    responses={
        200: DashboardSerializer,
        401: OpenApiResponse(
            response=ErrorSerializer,
            description="Authentication credentials are missing or invalid.",
        ),
    },
    summary="Get application statistics",
)
