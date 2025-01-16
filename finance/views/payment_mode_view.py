from django.core.cache import cache
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

# Import serializers
from ..serializers.payment_mode_serializer import (
    PaymentModeListSerializer,
    CreatePaymentModeSerializer,
    RetrievePaymentModeSerializer,
    UpdatePaymentModeSerializer,
)
from ..models import PaymentMode
from rest_framework.pagination import PageNumberPagination
import logging
from users.authentication import ExpiringTokenAuthentication
from rest_framework.permissions import IsAdminUser
from drf_spectacular.utils import extend_schema, extend_schema_view


class PaymentModePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 25


@extend_schema_view(
    list=extend_schema(
        operation_id="Payment Modes List",
        description="Gives list of payment modes",
    ),
    create=extend_schema(
        operation_id="Create Payment Mode",
        request={
            "multipart/form-data": CreatePaymentModeSerializer,
            "application/json": CreatePaymentModeSerializer,
        },
        description="Creates a payment mode.",
    ),
    retrieve=extend_schema(operation_id="View Payment Mode"),
    update=extend_schema(
        operation_id="Update Payment Mode",
        request={
            "multipart/form-data": UpdatePaymentModeSerializer,
            "application/json": UpdatePaymentModeSerializer,
        },
        description="Updates a payment mode.",
    ),
    destroy=extend_schema(
        operation_id="Delete Payment Mode",
        description="Deletes a payment mode.",
    ),
)
class PaymentModeViewSet(ViewSet):
    authentication_classes = [ExpiringTokenAuthentication]
    permission_classes = [IsAdminUser]

    def list(self, request):
        # Cache key for the list of payment modes
        cache_key = "payment_modes_list"

        # Try to get the cached payment modes list
        cached_payment_modes = cache.get(cache_key)
        if cached_payment_modes:
            return Response(cached_payment_modes, status.HTTP_200_OK)

        # If not cached, fetch the payment modes and cache the result
        payment_modes = PaymentMode.objects.all()
        serialized_data = PaymentModeListSerializer(
            payment_modes, many=True
        ).data
        paginator = PaymentModePagination()
        paginated_payment_modes = paginator.paginate_queryset(
            payment_modes, request
        )

        # Cache the paginated payment modes for 10 minutes
        cache.set(cache_key, serialized_data)

        return paginator.get_paginated_response(serialized_data)

    def create(self, request):
        serializer = CreatePaymentModeSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors, status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        payment_mode = PaymentMode()
        payment_mode.name = serializer.validated_data["name"]
        payment_mode.status = serializer.validated_data["status"]

        try:
            payment_mode.save()
        except Exception as e:
            logger = logging.getLogger("custom")
            logger.error(f"Payment Mode Creation Failed: {str(e)}")
            return Response(
                {"msg": "Payment Mode Creation Failed"},
                status.HTTP_417_EXPECTATION_FAILED,
            )
        return Response(
            {"msg": "Payment Mode Created Successfully"},
            status.HTTP_201_CREATED,
        )

    def retrieve(self, request, pk):
        # Cache key for individual payment mode
        cache_key = f"payment_mode_{pk}_cache"

        # Try to get the cached payment mode
        cached_result = cache.get(cache_key)
        if cached_result:
            return Response(cached_result, status.HTTP_200_OK)

        # Otherwise, fetch the payment mode and serialize it
        payment_mode = get_object_or_404(PaymentMode, id=pk)
        serialized_data = RetrievePaymentModeSerializer(payment_mode).data

        # Cache the individual payment mode for 10 minutes
        cache.set(cache_key, serialized_data)

        return Response(serialized_data, status.HTTP_200_OK)

    def update(self, request, pk):
        serializer = UpdatePaymentModeSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        try:
            payment_mode = get_object_or_404(PaymentMode, pk=pk)
            payment_mode.name = serializer.validated_data["name"]
            payment_mode.status = serializer.validated_data["status"]
            payment_mode.save()
        except Exception as e:
            logger = logging.getLogger("custom")
            logger.error(f"Payment Mode Update Failed: {str(e)}")
            return Response(
                {"msg": "Payment mode update Failed"},
                status=status.HTTP_417_EXPECTATION_FAILED,
            )

        # Invalidate the cache for both the specific payment mode and the list cache
        cache.delete(f"payment_mode_{pk}_cache")
        cache.delete("payment_modes_list")

        return Response(
            {"msg": "Payment Mode Update Successfully"},
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, pk):
        payment_mode = get_object_or_404(PaymentMode, pk=pk)

        try:
            payment_mode.delete()
        except Exception as e:
            logger = logging.getLogger("custom")
            logger.error(f"Payment Mode Deletion Failed: {str(e)}")
            return Response(
                {"msg": "Payment Mode Deletion Failed"},
                status=status.HTTP_417_EXPECTATION_FAILED,
            )

        # Invalidate the cache for both the specific payment mode and the list cache
        cache.delete(f"payment_mode_{pk}_cache")
        cache.delete("payment_modes_list")

        return Response(None, status.HTTP_204_NO_CONTENT)
