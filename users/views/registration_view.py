from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
import logging
from ..serializers.user_serializer import CreateUserSerializer
from ..models import CustomUser
from drf_spectacular.utils import extend_schema


@extend_schema(
    operation_id="Self Registration",
    request={
        "multipart/form-data": CreateUserSerializer,
        "application/json": CreateUserSerializer,
    },
    description="This endpoint allows user to register by themselves",
)
@api_view(["POST"])
def register_user(request):
    serializer = CreateUserSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors)

    try:
        CustomUser.objects.create_user(
            username=serializer.validated_data["username"],
            email=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
            mobile_number=serializer.validated_data.get("mobile_number"),
        )
    except Exception as e:
        logging.getLogger("django").error(f"Failed to register user: {str(e)}")
        return Response(
            "Registration Failed", status.HTTP_417_EXPECTATION_FAILED
        )
    return Response(
        {"msg": "User registered Successfully"}, status.HTTP_201_CREATED
    )
