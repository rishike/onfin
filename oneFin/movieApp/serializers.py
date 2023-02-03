from rest_framework import serializers


class MovieSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=1000)
    genres = serializers.CharField(max_length=100)
    uuid = serializers.UUIDField()
    