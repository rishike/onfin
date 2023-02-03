from rest_framework import serializers
from .models import Collection, Movies


class MoviesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
        fields = ("title", "description", "genres", "uuid")
        
class CollectionSerializer(serializers.ModelSerializer):
    movies = MoviesSerializer(many=True)
    class Meta:
        model = Collection
        fields = ("title", "description", "movies")