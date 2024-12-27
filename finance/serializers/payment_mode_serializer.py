from rest_framework import serializers
from ..models import PaymentMode


class PaymentModeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMode
        fields = "__all__"


class CreatePaymentModeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=30)
    status = serializers.BooleanField(required=True)

    class Meta:
        model = PaymentMode
        fields = "__all__"


class RetrievePaymentModeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)

    class Meta:
        model = PaymentMode
        fields = "__all__"


class UpdatePaymentModeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=30)
    status = serializers.BooleanField(required=True)

    class Meta:
        model = PaymentMode
        fields = "__all__"
