from rest_framework import serializers
from ..models import CustomUser
from rest_framework.validators import UniqueValidator
from django.core.validators import RegexValidator


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ["password"]


class CreateUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, max_length=30)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())],
    )
    password = serializers.CharField(required=True, max_length=30)
    mobile_number = serializers.CharField(
        required=True,
        validators=[
            RegexValidator(
                regex=r"^\d{10}$",
                message="Mobile number must be exactly 10 digits.",
            )
        ],
    )
    is_superuser = serializers.BooleanField(required=False, default=False)

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "email",
            "password",
            "mobile_number",
            "is_superuser",
        ]


class RetrieveUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)

    class Meta:
        model = CustomUser
        exclude = ["password"]


class UpdateUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, max_length=30)
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=CustomUser.objects.all(),
                lookup="iexact",  # Case-insensitive lookup if needed
                message="This email is already taken.",
            )
        ],
    )
    password = serializers.CharField(required=True, max_length=30)
    mobile_number = serializers.CharField(
        required=True,
        validators=[
            RegexValidator(
                regex=r"^\d{10}$",
                message="Mobile number must be exactly 10 digits.",
            )
        ],
    )
    is_superuser = serializers.BooleanField(required=False, default=False)

    class Meta:
        model = CustomUser
        fields = [
            "username",
            "email",
            "password",
            "mobile_number",
            "is_superuser",
        ]
