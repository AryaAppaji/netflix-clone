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


class SubscriptionPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page"
    max_page_size = 25


class SubscriptionViewSet(ViewSet):
    authentication_classes = [ExpiringTokenAuthentication]
    permission_classes = [IsAdminUser]

    def list(self, request):
        subscriptions = Subscription.objects.all()
        serialized_data = SubscriptionListSerializer(
            subscriptions, many=True
        ).data
        paginator = SubscriptionPagination()
        paginator.paginate_queryset(subscriptions, request)

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
        subscription = get_object_or_404(Subscription, pk=pk)
        serialized_data = RetrieveSubscriptionSerializer(subscription).data
        return Response(serialized_data, status=status.HTTP_200_OK)

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
        return Response(
            {"msg": "Subscription Created Successfully"}, status.HTTP_200_OK
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
        return Response(None, status.HTTP_204_NO_CONTENT)
