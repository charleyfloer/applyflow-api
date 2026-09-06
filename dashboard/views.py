from django.db.models import Count
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from applications.models import Application


class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        applications = Application.objects.filter(user=request.user)

        status_counts = applications.values("status").annotate(
            count=Count("id")
        )

        by_status = {
            status: 0
            for status, _ in Application.Status.choices
        }

        for item in status_counts:
            by_status[item["status"]] = item["count"]

        return Response({
            "total_applications": applications.count(),
            "by_status": by_status,
        })
