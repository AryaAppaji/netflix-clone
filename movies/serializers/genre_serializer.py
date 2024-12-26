from rest_framework import serializers
from ..models import Genre


class GenreListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class CreateGenreSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=30)
    status = serializers.BooleanField(required=True)

    class Meta:
        model = Genre
        fields = "__all__"


class RetrieveGenreSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)

    class Meta:
        model = Genre
        fields = "__all__"


class UpdateGenreSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=30)
    status = serializers.CharField(required=True)

    class Meta:
        model = Genre
        fields = "__all__"
