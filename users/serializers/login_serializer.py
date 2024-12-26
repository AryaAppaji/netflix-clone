from rest_framework import serializers
from ..models import CustomUser


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    device = serializers.CharField(required=True)


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ["password"]
