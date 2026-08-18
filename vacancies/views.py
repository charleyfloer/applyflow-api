from rest_framework.viewsets import ModelViewSet
from .models import Vacancy
from .serializers import VacancySerializer


class VacancyViewSet(ModelViewSet):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
