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


class PaymentModePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 25


class PaymentModeViewSet(ViewSet):
    authentication_classes = [ExpiringTokenAuthentication]

    def list(self, request):
        payment_modes = PaymentMode.objects.all()
        serialized_data = PaymentModeListSerializer(
            payment_modes, many=True
        ).data
        paginator = PaymentModePagination()
        paginator.paginate_queryset(payment_modes, request)

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
            logger = logging.getLogger("django")
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
        payment_mode = get_object_or_404(PaymentMode, id=pk)
        serialized_data = RetrievePaymentModeSerializer(payment_mode).data
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
            logger = logging.getLogger("django")
            logger.error(f"Payment Mode Update Failed: {str(e)}")
            return Response(
                {"msg": "Payment mode update Failed"},
                status=status.HTTP_417_EXPECTATION_FAILED,
            )

        return Response(
            {"msg": "Payment Mode Update Successfully"},
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, pk):
        payment_mode = get_object_or_404(PaymentMode, pk=pk)

        try:
            payment_mode.delete()
        except Exception as e:
            logger = logging.getLogger("django")
            logger.error(f"Payment Mode Deletion Failed: {str(e)}")
            return Response(
                {"msg": "Payment Mode Deletion Failed"},
                status.HTTP_417_EXPECTATION_FAILED,
            )

        return Response(None, status.HTTP_204_NO_CONTENT)
