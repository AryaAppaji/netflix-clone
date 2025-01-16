from django.core.cache import cache
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

# Import serializers
from ..serializers.subscription_serializer import (
    SubscriptionListSerializer,
    CreateSubscriptionSerializer,
    RetrieveSubscriptionSerializer,
    UpdateSubscriptionSerializer,
)
from rest_framework.pagination import PageNumberPagination
import logging
from ..models import Subscription
from users.authentication import ExpiringTokenAuthentication
from rest_framework.permissions import IsAdminUser
from drf_spectacular.utils import extend_schema, extend_schema_view


class SubscriptionPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page"
    max_page_size = 25


@extend_schema_view(
    list=extend_schema(
        operation_id="Subscriptions List",
        description="Gives list of subscriptions",
    ),
    create=extend_schema(
        operation_id="Create Subscription",
        request={
            "multipart/form-data": CreateSubscriptionSerializer,
            "application/json": CreateSubscriptionSerializer,
        },
        description="Creates a subscription.",
    ),
    retrieve=extend_schema(operation_id="View Subscription"),
    update=extend_schema(
        operation_id="Update Subscription",
        request={
            "multipart/form-data": UpdateSubscriptionSerializer,
            "application/json": UpdateSubscriptionSerializer,
        },
        description="Updates a subscription.",
    ),
    destroy=extend_schema(
        operation_id="Delete Subscription",
        description="Deletes a subscription.",
    ),
)
class SubscriptionViewSet(ViewSet):
    authentication_classes = [ExpiringTokenAuthentication]
    permission_classes = [IsAdminUser]

    def list(self, request):
        # Cache key for the list of subscriptions
        cache_key = "subscriptions_list"

        # Try to get the cached subscriptions list
        cached_subscriptions = cache.get(cache_key)
        if cached_subscriptions:
            return Response(cached_subscriptions, status.HTTP_200_OK)

        # If not cached, fetch the subscriptions and cache the result
        subscriptions = Subscription.objects.all()
        serialized_data = SubscriptionListSerializer(
            subscriptions, many=True
        ).data
        paginator = SubscriptionPagination()
        paginated_subscriptions = paginator.paginate_queryset(
            subscriptions, request
        )

        # Cache the paginated subscriptions for 10 minutes
        cache.set(cache_key, serialized_data)

        return paginator.get_paginated_response(serialized_data)

    def create(self, request):
        serializer = CreateSubscriptionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        subscription = Subscription()
        subscription.name = serializer.validated_data["name"]
        subscription.price = serializer.validated_data["price"]
        subscription.validity = serializer.validated_data["validity"]

        try:
            subscription.save()
        except Exception as e:
            logger = logging.getLogger("custom")
            logger.error(f"Subscription creation Failed: {str(e)}")
            return Response(
                {"msg": "Failed to create subscription"},
                status.HTTP_417_EXPECTATION_FAILED,
            )
        return Response(
            {"msg": "Subscription Created Successfully"},
            status.HTTP_201_CREATED,
        )

    def retrieve(self, request, pk):
        # Cache key for individual subscription
        cache_key = f"subscription_{pk}_cache"

        # Try to get the cached subscription
        cached_result = cache.get(cache_key)
        if cached_result:
            return Response(cached_result, status.HTTP_200_OK)

        # Otherwise, fetch the subscription and serialize it
        subscription = get_object_or_404(Subscription, pk=pk)
        serialized_data = RetrieveSubscriptionSerializer(subscription).data

        # Cache the individual subscription for 10 minutes
        cache.set(cache_key, serialized_data)

        return Response(serialized_data, status.HTTP_200_OK)

    def update(self, request, pk):
        serializer = UpdateSubscriptionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        subscription = get_object_or_404(Subscription, pk=pk)
        subscription.name = serializer.validated_data["name"]
        subscription.price = serializer.validated_data["price"]
        subscription.validity = serializer.validated_data["validity"]

        try:
            subscription.save()
        except Exception as e:
            logger = logging.getLogger("custom")
            logger.error(f"Subscription creation Failed: {str(e)}")
            return Response(
                {"msg": "Failed to create subscription"},
                status.HTTP_417_EXPECTATION_FAILED,
            )

        # Invalidate the cache for the specific subscription and the list cache
        cache.delete(f"subscription_{pk}_cache")
        cache.delete("subscriptions_list")

        return Response(
            {"msg": "Subscription Updated Successfully"}, status.HTTP_200_OK
        )

    def destroy(self, request, pk):
        subscription = get_object_or_404(Subscription, pk=pk)

        try:
            subscription.delete()
        except Exception as e:
            logger = logging.getLogger("custom")
            logger.error(f"Subscription Delete Failed:{str(e)}")
            return Response(
                {"msg": "Failed to delete subscription"},
                status.HTTP_417_EXPECTATION_FAILED,
            )

        # Invalidate the cache for the specific subscription and the list cache
        cache.delete(f"subscription_{pk}_cache")
        cache.delete("subscriptions_list")

        return Response(None, status.HTTP_204_NO_CONTENT)
