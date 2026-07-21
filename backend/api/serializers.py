from rest_framework import serializers


class ChatSerializer(serializers.Serializer):
    question = serializers.CharField()
    sources = serializers.ListField(
        child=serializers.CharField(),
        required=False,
        default=[],
    )


class DeleteFilesSerializer(serializers.Serializer):
    files = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=False,
    )
