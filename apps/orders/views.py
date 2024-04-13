from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Order, HistoryOrder
from .serializers import OrderSerializer, HistoryOrderSerializer
from .swagger import (
    get_order_response,
    get_history_order_response,
    get_path_request,
    cancel_order_response,
    cancel_order_request,
)
from ..main.models import City, Manufacturer
from ..parser.core import calculate_delivery_options
from ..products.models import Product


@extend_schema_view(
    get=extend_schema(
        responses=get_order_response,
        request=OrderSerializer,
        tags=["Order"],
    )
)
@api_view(["GET"])
def get_order_handler(request):
    """
    Обработчик получения заказов пользователя
    """

    orders = Order.objects.filter(user=request.user)
    orders_to_delete = orders.filter(status__in=["Delivered", "Rejection"])
    orders_to_delete.delete()
    serializer = OrderSerializer(orders, many=True)
    return Response({"data": serializer.data}, status=status.HTTP_200_OK)


@extend_schema(
    request=get_path_request,
    tags=["Order"],
)
@api_view(["POST"])
def get_path(request, pk):
    """
    Обработчик для получения путей заказа
    """

    try:
        product = get_object_or_404(Product, pk=pk)
    except:
        return Response({"error": {"code": 404, "message": "Not found"}})

    if product.status == "Out of stock":
        return Response({"error": "Продукта нет в наличии"})

    valid_city_name = request.session.get("valid_city_name")

    delivery_city_name = valid_city_name
    delivery_city = City.objects.get(name=delivery_city_name)

    company = Manufacturer.objects.get(name=product.company)
    delivery_options = calculate_delivery_options(company, delivery_city)

    best_path = delivery_options["best_path"]
    request.session["best_path"] = best_path

    return Response(
        {"data": {"path": best_path}},
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
def make_order(request, pk):
    """
    Функция для оформления заказа
    """
    try:
        product = get_object_or_404(Product, pk=pk)
    except:
        return Response({"error": {"code": 404, "message": "Not found"}})

    valid_city_name = request.session.get("valid_city_name")
    best_path = request.session.get("best_path")

    if not (product and request.user and valid_city_name and best_path):
        return Response(
            {"error": "Недостаточно данных для оформления заказа"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    order = Order.objects.create(
        user=request.user,
        city_name=valid_city_name,
        delivery_path=best_path["path"],
        status="Processed",
    )
    order.product.add(product)

    product.quantity -= 1
    product.save()

    return Response("Заказ оформлен", status=status.HTTP_201_CREATED)


@extend_schema(
    request=cancel_order_request,
    responses=cancel_order_response,
    tags=["Order"],
)
@api_view(["POST"])
def cancel_order(request, pk):
    try:
        order = Order.objects.get(user=request.user, pk=pk)
    except:
        return Response({"error": {"code": 404, "message": "Not found"}})

    text = request.data.get("text")
    if not text:
        return Response(
            {
                "error": {
                    "code": 400,
                    "message": "Необходимо указать причину отказа",
                }
            }
        )

    order.status = "Rejection"
    order.rejection_reason = text
    order.product.quantity += 1
    order.save()
    return Response({"success": True, "message": "Заказ отменен"})


@extend_schema_view(
    get=extend_schema(
        responses=get_history_order_response,
        request=HistoryOrderSerializer,
        tags=["Order"],
    )
)
@api_view(["GET"])
def history_orders(request):
    orders = Order.objects.filter(
        user=request.user, status__in=["Delivered", "Rejection"]
    )
    history_order = HistoryOrder.objects.create()
    history_order.orders.set(orders)
    serializer = HistoryOrderSerializer(history_order)
    return Response(serializer.data, status=status.HTTP_200_OK)
