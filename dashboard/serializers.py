from rest_framework import serializers


class ApplicationStatusCountsSerializer(serializers.Serializer):
    saved = serializers.IntegerField(min_value=0)
    applied = serializers.IntegerField(min_value=0)
    screening = serializers.IntegerField(min_value=0)
    interview = serializers.IntegerField(min_value=0)
    offer = serializers.IntegerField(min_value=0)
    rejected = serializers.IntegerField(min_value=0)
    withdrawn = serializers.IntegerField(min_value=0)


class DashboardSerializer(serializers.Serializer):
    total_applications = serializers.IntegerField(min_value=0)
    by_status = ApplicationStatusCountsSerializer()
