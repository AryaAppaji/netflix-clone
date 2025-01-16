from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.shortcuts import get_object_or_404
from ..serializers.movie_serializer import (
    MovieListSerializer,
    CreateMovieSerializer,
    RetrieveMovieSerializer,
    UpdateMovieSerializer,
)
from rest_framework.pagination import PageNumberPagination
from ..models import Movie
from finance.models import UserSubscription
import logging
from users.authentication import ExpiringTokenAuthentication
from django.utils.timezone import now
from rest_framework.permissions import AllowAny, IsAdminUser
from drf_spectacular.utils import extend_schema, extend_schema_view
import os
from django.core.cache import cache


class MoviePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"


@extend_schema_view(
    list=extend_schema(
        operation_id="Movies List", description="Gives list of movies"
    ),
    create=extend_schema(
        operation_id="Create Movies",
        request={
            "multipart/form-data": CreateMovieSerializer,
        },
        description="Creates a movie.",
    ),
    retrieve=extend_schema(operation_id="View Movie"),
    update=extend_schema(
        operation_id="Update Movie",
        request={
            "multipart/form-data": UpdateMovieSerializer,
        },
        description="Updates a movie.",
    ),
    destroy=extend_schema(
        operation_id="Delete Movie", description="Deletes a movie."
    ),
)
class MovieViewSet(ViewSet):
    authentication_classes = [ExpiringTokenAuthentication]
    permission_classes = [IsAdminUser]
    logger = logging.getLogger("custom")

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]

    def list(self, request):
        if not request.user.is_superuser:
            subscription = UserSubscription.objects.filter(
                user=request.user, is_current_subscription=True
            ).first()

            if not subscription:
                return Response(
                    {
                        "msg": "You don't have any subscription till now, Please purchase one"
                    },
                    status.HTTP_400_BAD_REQUEST,
                )

            if now() > subscription.end_date:
                return Response(
                    {
                        "msg": "Your current subscription was expired, Please purchase new one"
                    },
                    status.HTTP_400_BAD_REQUEST,
                )

        movies = Movie.objects.all()
        paginator = MoviePagination()
        paginated_movies = paginator.paginate_queryset(movies, request)
        serialized_data = MovieListSerializer(paginated_movies, many=True).data
        return paginator.get_paginated_response(serialized_data)

    def create(self, request):
        serializer = CreateMovieSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        try:
            # Create movie instance first (without the file)
            movie = Movie(
                name=serializer.validated_data["name"],
                release_year=serializer.validated_data["release_year"],
                description=serializer.validated_data["description"],
            )
            movie.save()  # Save to generate an ID

            # Add genres
            movie.genres.add(*serializer.validated_data["genres"])

            file = request.FILES.get("file")
            movie.file = file
            movie.save()

        except Exception as e:
            self.logger.error(f"Movie Creation Failed: {str(e)}")
            return Response(
                {"msg": "Failed to upload movie"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"msg": "Movie uploaded successfully"},
            status=status.HTTP_201_CREATED,
        )

    def retrieve(self, request, pk):
        # Cache key for an individual movie
        cache_key = f"movie_{pk}_cache"

        # Try to get the cached movie
        cached_result = cache.get(cache_key)
        if cached_result:
            # Return the cached movie if available
            return Response(cached_result, status.HTTP_200_OK)

        # Otherwise, fetch the movie and serialize
        movie = get_object_or_404(Movie, pk=pk)
        serialized_data = RetrieveMovieSerializer(movie).data

        # Cache the individual movie for 10 minutes
        cache.set(cache_key, serialized_data)

        return Response(serialized_data, status.HTTP_200_OK)

    def update(self, request, pk):
        serializer = UpdateMovieSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        movie = get_object_or_404(Movie, pk=pk)

        movie.name = serializer.validated_data["name"]
        movie.release_year = serializer.validated_data["release_year"]
        movie.description = serializer.validated_data["description"]

        try:
            if "genres" in serializer.validated_data:
                movie.genres.set(serializer.validated_data["genres"])

            # Handle file upload (file is required)
            new_file = request.FILES["file"]

            # Delete the old file
            if movie.file and movie.file.name:
                old_file_path = os.path.join(
                    settings.MEDIA_ROOT, movie.file.name
                )
                if os.path.exists(old_file_path):
                    os.remove(old_file_path)

            movie.file = new_file

            movie.save()

        except Exception as e:
            self.logger.error(f"Movie Update Failed: {str(e)}")
            return Response(
                {"msg": "Failed to update movie"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Invalidate both the specific movie and movie list cache
        cache.delete(f"movie_{pk}_cache")

        return Response(
            {"msg": "Movie updated successfully"},
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, pk):
        movie = get_object_or_404(Movie, pk=pk)

        try:
            movie.delete()
        except Exception as e:
            self.logger.error(f"Movie Deletion Failed: {str(e)}")
            return Response(
                {"msg": "Failed to delete movie"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Invalidate both the specific movie and movie list cache
        cache.delete(f"movie_{pk}_cache")

        return Response(None, status.HTTP_204_NO_CONTENT)
