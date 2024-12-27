from rest_framework import serializers
from ..models import Subscription


class SubscriptionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"


class CreateSubscriptionSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=30)
    price = serializers.FloatField(required=True)
    validity = serializers.IntegerField(required=True)

    class Meta:
        model = Subscription
        fields = "__all__"


class RetrieveSubscriptionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)

    class Meta:
        model = Subscription
        fields = "__all__"


class UpdateSubscriptionSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=30)
    price = serializers.FloatField(required=True)
    validity = serializers.IntegerField(required=True)

    class Meta:
        model = Subscription
        fields = "__all__"
