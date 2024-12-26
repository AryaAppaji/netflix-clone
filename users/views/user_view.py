from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ..models import CustomUser
import logging

# Import serializers
from ..serializers.user_serializer import (
    UserListSerializer,
    CreateUserSerializer,
    RetrieveUserSerializer,
    UpdateUserSerializer,
)

from rest_framework.pagination import PageNumberPagination
from users.authentication import ExpiringTokenAuthentication


class UserPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 25


class UserViewSet(ViewSet):
    pagination_class = UserPagination  # Add this line to use pagination_class
    authentication_classes = [ExpiringTokenAuthentication]

    def list(self, request):
        users = CustomUser.objects.filter()
        paginator = self.pagination_class()  # Use the pagination class here
        paginated_users = paginator.paginate_queryset(
            users, request
        )  # Apply pagination
        serialized_data = UserListSerializer(paginated_users, many=True).data
        return paginator.get_paginated_response(
            serialized_data
        )  # Return paginated response

    def create(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        try:
            CustomUser.objects.create_user(
                username=serializer.validated_data["username"],
                email=serializer.validated_data["email"],
                password=serializer.validated_data["password"],
                mobile_number=serializer.validated_data.get(
                    "mobile_number"
                ),  # Correct field
            )
        except Exception as e:
            logger = logging.getLogger("django")
            logger.error(f"User Creation Failed: {str(e)}")
            return Response(
                {"msg": "Registration Failed"},
                status.HTTP_417_EXPECTATION_FAILED,
            )

        return Response(
            {"msg": "Registered Successfully"}, status.HTTP_201_CREATED
        )

    def retrieve(self, request, pk):
        # Directly use get_object_or_404 to raise 404 if user not found
        user = get_object_or_404(CustomUser, id=pk)
        serialized_data = RetrieveUserSerializer(user).data
        return Response(serialized_data, status.HTTP_200_OK)

    def update(self, request, pk):
        # Retrieve the user object
        user = get_object_or_404(CustomUser, id=pk)

        # Use UpdateUserSerializer (if needed) for validation
        serializer = UpdateUserSerializer(
            user, data=request.data, partial=True
        )  # partial=True allows partial updates
        if not serializer.is_valid():
            return Response(
                serializer.errors, status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        try:
            # Update fields and save user
            user.username = serializer.validated_data.get(
                "username", user.username
            )
            user.email = serializer.validated_data.get("email", user.email)
            if "password" in serializer.validated_data:
                user.set_password(
                    serializer.validated_data["password"]
                )  # Use `set_password` for passwords
            user.mobile_number = serializer.validated_data.get(
                "mobile_number", user.mobile_number
            )
            user.save()

        except Exception as e:
            logger = logging.getLogger("django")
            logger.error(f"User Update Failed: {str(e)}")
            return Response(
                {"msg": "User update failed"},
                status.HTTP_417_EXPECTATION_FAILED,
            )

        return Response(
            {"msg": "User updated successfully"}, status.HTTP_200_OK
        )

    def destroy(self, request, pk):
        user = get_object_or_404(CustomUser, id=pk)
        try:
            user.delete()
        except Exception as e:
            logger = logging.getLogger("django")
            logger.error(f"User Deletion Failed: {str(e)}")
            return Response(
                {"msg": "User Deletion Failed"},
                status.HTTP_417_EXPECTATION_FAILED,
            )

        return Response(None, status.HTTP_204_NO_CONTENT)
