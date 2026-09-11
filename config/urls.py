from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path('admin/', admin.site.urls),
    path("api/users/", include("users.urls")),
    path("api/companies/", include("companies.urls")),
    path("api/vacancies/", include("vacancies.urls")),
    path("api/applications/", include("applications.urls")),
    path("api/interviews/", include("interviews.urls")),
    path("api/dashboard/", include("dashboard.urls")),
]
