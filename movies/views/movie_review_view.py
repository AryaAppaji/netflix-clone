from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

# Import serializers
from ..serializers.movie_review_serializer import (
    MovieReviewListSerializer,
    CreateMovieReviewSerializer,
    RetrieveMovieReviewSerializer,
    UpdateMovieReviewSerializer,
)
from rest_framework.pagination import PageNumberPagination
from ..models import Review
from users.models import ExpiringToken
import logging
from users.authentication import ExpiringTokenAuthentication


class MovieReviewPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"


class MovieReviewViewSet(ViewSet):
    authentication_classes = [ExpiringTokenAuthentication]

    def list(self, request):
        movies = Review.objects.all()
        paginator = MovieReviewPagination()
        paginated_movies = paginator.paginate_queryset(movies, request)
        serialized_data = MovieReviewListSerializer(
            paginated_movies, many=True
        ).data
        return paginator.get_paginated_response(serialized_data)

    def create(self, request):
        serializer = CreateMovieReviewSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors, status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        request_token = request.headers.get("Authorization").split()[1]
        token = ExpiringToken.objects.get(key=request_token)

        review = Review()
        review.user = token.user
        review.movie = serializer.validated_data["movie"]
        review.rating = serializer.validated_data["rating"]
        review.content = serializer.validated_data["content"]
        try:
            review.save()
        except Exception as e:
            logger = logging.getLogger("django")
            logger.error(f"Review Cretion Failed:{str(e)}")
            return Response(
                {"msg": "Failed to add review"},
                status.HTTP_417_EXPECTATION_FAILED,
            )
        return Response(
            {"msg": "Review added successfully"},
            status.HTTP_417_EXPECTATION_FAILED,
        )

    def retrieve(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        return Response(
            RetrieveMovieReviewSerializer(review).data, status.HTTP_200_OK
        )

    def update(self, request, pk):
        serializer = UpdateMovieReviewSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors, status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        review = get_object_or_404(Review, pk=pk)
        review.rating = serializer.validated_data["rating"]
        review.content = serializer.validated_data["content"]
        try:
            review.save()
        except Exception as e:
            logger = logging.getLogger("django")
            logger.error(f"Review Cretion Failed:{str(e)}")
            return Response(
                {"msg": "Failed to add review"},
                status.HTTP_417_EXPECTATION_FAILED,
            )
        return Response(
            {"msg": "Review updated successfully"},
            status.HTTP_200_OK,
        )

    def destroy(self, request, pk):
        review = get_object_or_404(Review, pk=pk)

        try:
            review.delete()
        except Exception as e:
            logger = logging.getLogger("django")
            logger.error(f"Review Deletion Failed:{str(e)}")
            return Response(
                {"msg": "Failed to delete review"},
                status.HTTP_417_EXPECTATION_FAILED,
            )
        return Response(None, status.HTTP_417_EXPECTATION_FAILED)
