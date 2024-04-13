from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .serializers import LogSerializer, RegSerializer, ApplicationSerializer
from .swagger import login_response, reg_response, applications_response
from ..main.models import Manufacturer, City


@api_view(["POST"])
def logout(request):
    request.user.auth_token.delete()
    return Response({"message": "Log out"}, status=status.HTTP_200_OK)


@extend_schema_view(
    post=extend_schema(
        responses=login_response,
        request=LogSerializer,
        tags=["Auth"],
    )
)
@api_view(["POST"])
def login(request):
    serializer = LogSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data.get("user")
        try:
            if not user:
                return Response(
                    {
                        "error": {
                            "code": status.HTTP_401_UNAUTHORIZED,
                            "message": "Authentication failed",
                        }
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            else:
                token, created = Token.objects.get_or_create(user=user)
                return Response(
                    {"data": {"user_token": token.key}},
                    status=status.HTTP_200_OK,
                )
        except:
            return Response(
                {
                    "error": {
                        "message": "User with this email or "
                        "password does not exist"
                    }
                }
            )
    return Response(
        {
            "error": {
                "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                "message": "Validation error",
                "errors": serializer.errors,
            }
        },
        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


@extend_schema_view(
    post=extend_schema(
        responses=reg_response,
        request=RegSerializer,
        tags=["Auth"],
    )
)
@api_view(["POST"])
def registration(request):
    serializer = RegSerializer(data=request.data, context={"request": request})
    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.create(user=user)
        return Response(
            {
                "data": {
                    "user_token": token.key,
                }
            },
            status=status.HTTP_201_CREATED,
        )
    return Response(
        {
            "error": {
                "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                "message": "Validation error",
                "errors": serializer.errors,
            }
        },
        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


@extend_schema_view(
    post=extend_schema(
        responses=applications_response,
        request=ApplicationSerializer,
        tags=["Other"],
    )
)
@api_view(["POST"])
def company_application(request):
    """
    Отправка заявки на то, что пользователь является компанией
    """
    name = request.data.get("name", "")
    city_names = [city.lower() for city in request.data.get("cities", [])]
    user = request.user

    if Manufacturer.objects.filter(name__iexact=name).exists():
        raise ValidationError("Компания с таким именем уже существует")

    cities = []
    not_found_cities = []
    for city_name in city_names:
        try:
            city = City.objects.get(name__iexact=city_name)
            cities.append(city.id)
        except City.DoesNotExist:
            not_found_cities.append(city_name)

    if not_found_cities:
        return Response(
            {"detail": f"Города не найдены: {', '.join(not_found_cities)}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    serializer_data = {
        "name": name,
        "user": user.id,
        "cities": cities,
    }

    serializer = ApplicationSerializer(data=serializer_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
