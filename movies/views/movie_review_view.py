from django.core.cache import cache
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
from rest_framework.permissions import IsAdminUser
from drf_spectacular.utils import extend_schema, extend_schema_view


class MovieReviewPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"


@extend_schema_view(
    list=extend_schema(
        operation_id="Reviews List", description="Gives list of reviews"
    ),
    create=extend_schema(
        operation_id="Create Review",
        request={
            "multipart/form-data": CreateMovieReviewSerializer,
            "application/json": CreateMovieReviewSerializer,
        },
        description="Creates a review.",
    ),
    retrieve=extend_schema(operation_id="View Review"),
    update=extend_schema(
        operation_id="Update Review",
        request={
            "multipart/form-data": UpdateMovieReviewSerializer,
            "application/json": UpdateMovieReviewSerializer,
        },
        description="Updates a review.",
    ),
    destroy=extend_schema(
        operation_id="Delete Review", description="Deletes a review."
    ),
)
class MovieReviewViewSet(ViewSet):
    authentication_classes = [ExpiringTokenAuthentication]
    permission_classes = [IsAdminUser]

    def list(self, request):
        # Cache key for the list of reviews
        cache_key = "movie_reviews_list"

        # Try to get the cached list
        cached_reviews = cache.get(cache_key)
        if cached_reviews:
            return Response(cached_reviews, status.HTTP_200_OK)

        # If not cached, fetch the reviews and cache the result
        reviews = Review.objects.all()
        paginator = MovieReviewPagination()
        paginated_reviews = paginator.paginate_queryset(reviews, request)
        serialized_data = MovieReviewListSerializer(
            paginated_reviews, many=True
        ).data

        # Cache the paginated reviews for 10 minutes
        cache.set(cache_key, serialized_data)

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
            logger = logging.getLogger("custom")
            logger.error(f"Review Creation Failed:{str(e)}")
            return Response(
                {"msg": "Failed to add review"},
                status.HTTP_417_EXPECTATION_FAILED,
            )
        return Response(
            {"msg": "Review added successfully"},
            status.HTTP_201_CREATED,
        )

    def retrieve(self, request, pk):
        # Cache key for individual review
        cache_key = f"movie_review_{pk}_cache"

        # Try to get the cached review
        cached_result = cache.get(cache_key)
        if cached_result:
            return Response(cached_result, status.HTTP_200_OK)

        # Otherwise, fetch the review and serialize
        review = get_object_or_404(Review, pk=pk)
        serialized_data = RetrieveMovieReviewSerializer(review).data

        # Cache the individual review for 10 minutes
        cache.set(cache_key, serialized_data)

        return Response(serialized_data, status.HTTP_200_OK)

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
            logger = logging.getLogger("custom")
            logger.error(f"Review Creation Failed:{str(e)}")
            return Response(
                {"msg": "Failed to update review"},
                status.HTTP_417_EXPECTATION_FAILED,
            )

        # Invalidate both the cached review and the list cache
        cache.delete(f"movie_review_{pk}_cache")
        cache.delete("movie_reviews_list")

        return Response(
            {"msg": "Review updated successfully"},
            status.HTTP_200_OK,
        )

    def destroy(self, request, pk):
        review = get_object_or_404(Review, pk=pk)

        try:
            review.delete()
        except Exception as e:
            logger = logging.getLogger("custom")
            logger.error(f"Review Deletion Failed:{str(e)}")
            return Response(
                {"msg": "Failed to delete review"},
                status.HTTP_417_EXPECTATION_FAILED,
            )

        # Invalidate both the cached review and the list cache
        cache.delete(f"movie_review_{pk}_cache")
        cache.delete("movie_reviews_list")

        return Response(None, status.HTTP_204_NO_CONTENT)
