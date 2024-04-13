from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .swagger import get_city_name_response, get_city_name_request
from ..main.models import City
from ..products.models import Product


def validate_city_name(city_name):
    """
    Получение имени города введённый пользователем
    """
    try:
        city = City.objects.get(name__iexact=city_name)
        return city.name
    except City.DoesNotExist:
        return None


@extend_schema(
    request=get_city_name_request,
    responses=get_city_name_response,
    tags=["Order"],
)
@api_view(["POST"])
def get_city_name(request, pk):
    """
    Функция получения города введённый пользователем
    """
    try:
        product = get_object_or_404(Product, pk=pk)
    except:
        return Response({"error": {"code": 404, "message": "Not found"}})

    if product.status == "Out of stock":
        return Response({"error": "Продукта нет в наличии"})

    city_name = request.data.get("city_name").lower()
    if not city_name:
        return Response(
            {"error": "Не указано название города"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    valid_city_name = validate_city_name(city_name)
    if valid_city_name:
        request.session["valid_city_name"] = valid_city_name
        return Response(
            "Название города с пвз занесён в заказ", status=status.HTTP_200_OK
        )
    else:
        return Response(
            {"error": f"Город '{city_name}' не найден в списке"},
            status=status.HTTP_404_NOT_FOUND,
        )
