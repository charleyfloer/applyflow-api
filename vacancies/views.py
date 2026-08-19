from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Vacancy
from .serializers import VacancySerializer


class VacancyViewSet(ModelViewSet):
    queryset = Vacancy.objects.select_related("company")
    serializer_class = VacancySerializer
    permission_classes = [IsAuthenticated]
