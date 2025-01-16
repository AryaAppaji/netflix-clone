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
from django.core.cache import cache


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
        paginator = UserPagination()
        # Cache key for paginated user list
        cache_key = "user_list_cache"

        # Try to get the cached result
        cached_result = cache.get(cache_key)
        if cached_result:
            # Return cached result if it exists
            return Response(cached_result, status.HTTP_200_OK)

        # If not cached, fetch the users and serialize
        users = CustomUser.objects.all()

        paginated_users = paginator.paginate_queryset(users, request)
        serialized_data = UserListSerializer(paginated_users, many=True).data

        # Cache the result for 5 minutes
        cache.set(cache_key, serialized_data)

        # Return paginated response
        return paginator.get_paginated_response(serialized_data)

    def create(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors, status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        try:
            if serializer.validated_data["is_superuser"]:
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

        # Invalidate the cache for the user list
        cache.delete("user_list_cache")

        return Response(
            {"msg": "Registered Successfully"}, status.HTTP_201_CREATED
        )

    def retrieve(self, request, pk):
        # Cache key for retrieving user by ID
        cache_key = f"user_{pk}_cache"

        # Try to get the cached user data
        cached_result = cache.get(cache_key)
        if cached_result:
            # Return cached result if it exists
            return Response(cached_result, status.HTTP_200_OK)

        # If not cached, fetch the user and serialize
        user = get_object_or_404(CustomUser, id=pk)
        serialized_data = RetrieveUserSerializer(user).data

        # Cache the result for 10 minutes
        cache.set(cache_key, serialized_data)

        # Return the serialized user data
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

            # Invalidate cache for the specific user and the user list
            cache.delete(f"user_{pk}_cache")
            cache.delete("user_list_cache")
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
            # Invalidate cache for the specific user and the user list
            cache.delete(f"user_{pk}_cache")
            cache.delete("user_list_cache")
        except Exception as e:
            logger.error(f"User Deletion Failed: {str(e)}")
            return Response(
                {"msg": "User Deletion Failed"},
                status.HTTP_417_EXPECTATION_FAILED,
            )

        return Response(None, status.HTTP_204_NO_CONTENT)
