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
from rest_framework.permissions import IsAdminUser
from drf_spectacular.utils import extend_schema, extend_schema_view


# Pagination Class
class UserPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"


# Logger Initialization
logger = logging.getLogger("custom")


# User ViewSet
@extend_schema_view(
    list=extend_schema(
        operation_id="Users List", description="Gives list of users"
    ),
    create=extend_schema(
        operation_id="Create Users",
        request={
            "multipart/form-data": CreateUserSerializer,
            "application/json": CreateUserSerializer,
        },
        description="Creates a user.",
    ),
    retrieve=extend_schema(operation_id="View User"),
    update=extend_schema(
        operation_id="Update User",
        request={
            "multipart/form-data": UpdateUserSerializer,
            "application/json": UpdateUserSerializer,
        },
        description="Updates a user.",
    ),
    destroy=extend_schema(
        operation_id="Delete User", description="Deletes a user."
    ),
)
class UserViewSet(ViewSet):
    authentication_classes = [ExpiringTokenAuthentication]
    permission_classes = [IsAdminUser]
    pagination_class = UserPagination

    def list(self, request):
        users = CustomUser.objects.all()
        paginator = self.pagination_class()
        paginated_users = paginator.paginate_queryset(users, request)
        serialized_data = UserListSerializer(paginated_users, many=True).data
        return paginator.get_paginated_response(serialized_data)

    def create(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        try:
            if self.validated_data["is_superuser"]:
                CustomUser.objects.create_superuser(
                    username=serializer.validated_data["username"],
                    email=serializer.validated_data["email"],
                    password=serializer.validated_data["password"],
                    mobile_number=serializer.validated_data.get(
                        "mobile_number"
                    ),
                )
            else:
                CustomUser.objects.create_user(
                    username=serializer.validated_data["username"],
                    email=serializer.validated_data["email"],
                    password=serializer.validated_data["password"],
                    mobile_number=serializer.validated_data.get(
                        "mobile_number"
                    ),
                )
        except Exception as e:
            logger.error(f"User Creation Failed: {str(e)}")
            return Response(
                {"msg": "Registration Failed"},
                status.HTTP_417_EXPECTATION_FAILED,
            )

        return Response(
            {"msg": "Registered Successfully"}, status.HTTP_201_CREATED
        )

    def retrieve(self, request, pk):
        user = get_object_or_404(CustomUser, id=pk)
        serialized_data = RetrieveUserSerializer(user).data
        return Response(serialized_data, status.HTTP_200_OK)

    def update(self, request, pk):
        user = get_object_or_404(CustomUser, id=pk)
        serializer = UpdateUserSerializer(
            user, data=request.data, partial=True
        )
        if not serializer.is_valid():
            return Response(
                serializer.errors, status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        try:
            user.username = serializer.validated_data.get(
                "username", user.username
            )
            user.email = serializer.validated_data.get("email", user.email)
            if "password" in serializer.validated_data:
                user.set_password(serializer.validated_data["password"])
            user.mobile_number = serializer.validated_data.get(
                "mobile_number", user.mobile_number
            )
            user.is_superuser = serializer.validated_data.get(
                "is_superuser", False
            )
            user.save()
        except Exception as e:
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
            logger.error(f"User Deletion Failed: {str(e)}")
            return Response(
                {"msg": "User Deletion Failed"},
                status.HTTP_417_EXPECTATION_FAILED,
            )

        return Response(None, status.HTTP_204_NO_CONTENT)
