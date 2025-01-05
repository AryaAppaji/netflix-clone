from rest_framework import serializers
from ..models import Movie, Review
from users.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ["password"]


# Movie Serializer
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"


# Movie Review List Serializer (for Listing All Reviews with Nested Details)
class MovieReviewListSerializer(serializers.ModelSerializer):
    movie = MovieSerializer()
    user = UserSerializer()

    class Meta:
        model = Review
        fields = "__all__"


# Create Movie Review Serializer
class CreateMovieReviewSerializer(serializers.ModelSerializer):
    movie = serializers.PrimaryKeyRelatedField(
        queryset=Movie.objects.all(), required=True
    )
    rating = serializers.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    content = serializers.CharField(max_length=1000)

    class Meta:
        model = Review
        fields = ["movie", "rating", "content"]


# Retrieve Movie Review Serializer (for Retrieving a Single Review with Nested Details)
class RetrieveMovieReviewSerializer(serializers.ModelSerializer):
    movie = MovieSerializer()
    user = UserSerializer()

    class Meta:
        model = Review
        fields = "__all__"


# Update Movie Review Serializer
class UpdateMovieReviewSerializer(serializers.ModelSerializer):
    rating = serializers.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    content = serializers.CharField(max_length=1000)

    class Meta:
        model = Review
        fields = ["rating", "content"]
