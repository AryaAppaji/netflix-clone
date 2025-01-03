from rest_framework import serializers
from ..models import Movie, Genre
from django.core.validators import FileExtensionValidator


class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"


class CreateMovieSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=30)
    release_year = serializers.IntegerField(required=True)
    description = serializers.CharField(required=True, max_length=1000)
    genres = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(), many=True, required=True
    )
    file = serializers.FileField(
        validators=[FileExtensionValidator(allowed_extensions=["mp4"])],
        required=True,
    )

    class Meta:
        model = Movie
        fields = "__all__"


class RetrieveMovieSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)

    class Meta:
        model = Movie
        fields = "__all__"


class UpdateMovieSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=30)
    release_year = serializers.IntegerField(required=True)
    description = serializers.CharField(required=True, max_length=1000)
    genres = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(), many=True, required=True
    )
    file = serializers.FileField(
        validators=[FileExtensionValidator(allowed_extensions=["mp4"])],
        required=True,
    )

    class Meta:
        model = Movie
        fields = "__all__"
