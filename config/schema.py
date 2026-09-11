from rest_framework import serializers


class ErrorSerializer(serializers.Serializer):
    detail = serializers.CharField()


VALIDATION_ERROR_SCHEMA = {
    "type": "object",
    "additionalProperties": {
        "type": "array",
        "items": {"type": "string"},
    },
}
