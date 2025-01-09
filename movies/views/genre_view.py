from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
import logging
from ..models import Genre
from rest_framework.pagination import PageNumberPagination

# Import serializers
from ..serializers.genre_serializer import (
    GenreListSerializer,
    CreateGenreSerializer,
    RetrieveGenreSerializer,
    UpdateGenreSerializer,
)
from users.authentication import ExpiringTokenAuthentication
from rest_framework.permissions import IsAdminUser
from drf_spectacular.utils import extend_schema, extend_schema_view


class GenrePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 25


@extend_schema_view(
    list=extend_schema(
        operation_id="Movies List", description="Gives list of movies"
    ),
    create=extend_schema(
        operation_id="Create Movies",
        request={
            "multipart/form-data": CreateGenreSerializer,
            "application/json": CreateGenreSerializer,
        },
        description="Creates a movie.",
    ),
    retrieve=extend_schema(operation_id="View Movie"),
    update=extend_schema(
        operation_id="Update Movie",
        request={
            "multipart/form-data": UpdateGenreSerializer,
            "application/json": UpdateGenreSerializer,
        },
        description="Updates a movie.",
    ),
    destroy=extend_schema(
        operation_id="Delete Movie", description="Deletes a movie."
    ),
)
class GenreViewSet(ViewSet):
    authentication_classes = [ExpiringTokenAuthentication]
    permission_classes = [IsAdminUser]

    def list(self, request):
        genres = Genre.objects.all()
        serialized_data = GenreListSerializer(genres, many=True).data
        paginator = GenrePagination()
        paginator.paginate_queryset(genres, request)

        return paginator.get_paginated_response(serialized_data)

    def create(self, request):
        serializer = CreateGenreSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors, status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        genre = Genre()
        genre.name = serializer.validated_data["name"]
        genre.status = serializer.validated_data["status"]

        try:
            genre.save()
        except Exception as e:
            logger = logging.getLogger("custom")
            logger.error(f"Genre Creation Failed: {str(e)}")
            return Response(
                {"msg": "Genre Creation Failed"},
                status.HTTP_417_EXPECTATION_FAILED,
            )
        return Response(
            {"msg": "Genre Created Successfully"}, status.HTTP_201_CREATED
        )

    def retrieve(self, request, pk):
        genre = get_object_or_404(Genre, id=pk)
        serialized_data = RetrieveGenreSerializer(genre).data
        return Response(serialized_data, status.HTTP_200_OK)

    def update(self, request, pk):
        serializer = UpdateGenreSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        try:
            genre = get_object_or_404(Genre, pk=pk)
            genre.name = serializer.validated_data["name"]
            genre.status = serializer.validated_data["status"]
            genre.save()
        except Exception as e:
            logger = logging.getLogger("custom")
            logger.error(f"Genre Update Failed: {str(e)}")
            return Response(
                {"msg": str(e)}, status=status.HTTP_417_EXPECTATION_FAILED
            )

        return Response(
            {"msg": "Genre Update Successfully"}, status=status.HTTP_200_OK
        )

    def destroy(self, request, pk):
        genre = get_object_or_404(Genre, pk=pk)

        try:
            genre.delete()
        except Exception as e:
            logger = logging.getLogger("custom")
            logger.error(f"Genre Deletion Failed: {str(e)}")
            return Response(
                {"msg": "Genre Deletion Failed"},
                status.HTTP_417_EXPECTATION_FAILED,
            )

        return Response(None, status.HTTP_204_NO_CONTENT)
