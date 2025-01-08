from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from ..models import ExpiringToken
from ..serializers.login_serializer import LoginSerializer, UserDataSerializer
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.decorators import action


class AuthViewSet(ViewSet):
    @action(methods=["POST"], url_path="login", detail=False)
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )
        if not user or user is None:
            return Response(
                {"msg": "Invalid Credentials"}, status.HTTP_401_UNAUTHORIZED
            )
        ExpiringToken.objects.filter(user=user).delete()
        token = ExpiringToken.objects.create(
            user=user, expires_at=timezone.now() + timedelta(days=1)
        )

        return Response(
            {"user": UserDataSerializer(user).data, "token": token.key},
            status=status.HTTP_200_OK,
        )

    @action(methods=["POST"], url_path="logout", detail=False)
    def logout(self, request):
        authorization_header = request.headers.get("Authorization", "")

        # Check if the Authorization header is missing
        if not authorization_header:
            return Response(
                {"msg": "Authorization header missing"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token_key = authorization_header.split()[
                1
            ]  # Split and get the token
        except IndexError:
            return Response(
                {"msg": "Token is missing in the Authorization header"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Try to retrieve the token from the database
        try:
            token = ExpiringToken.objects.get(key=token_key)
            token.delete()  # Delete the token if it exists
        except ExpiringToken.DoesNotExist:
            return Response(
                {"msg": "Token not found in records"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Return a success message
        return Response(
            {"msg": "User logged out successfully."}, status=status.HTTP_200_OK
        )
