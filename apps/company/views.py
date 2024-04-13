from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import OrdersUser
from .serializers import OrdersUserSerializer
from .swagger import user_orders_response
from ..orders.models import Order


@extend_schema(
    request=OrdersUserSerializer,
    responses=user_orders_response,
    tags=["Other"]
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def orders_user(request):
    user = request.user

    if user.is_manufacturer:
        products = user.company.product.all()
        orders = Order.objects.filter(product__in=products)
        processed_orders = orders.filter(status__in=["Processed", "In path"])

        orders_user_inst, created = OrdersUser.objects.get_or_create(user=user)
        orders_user_inst.orders.set(processed_orders)

        serializer = OrdersUserSerializer(orders_user_inst)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(
            {"error": "Forbidden for you"}, status=status.HTTP_403_FORBIDDEN
        )


@api_view(["POST"])
def accept_order(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(
            {"error": "Not found"}, status=status.HTTP_404_NOT_FOUND
        )
    order.status = "Accepted"
    order.save()
    return Response({"message": "Заказ принят"}, status=status.HTTP_200_OK)


@api_view(["POST"])
def rejection_order(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(
            {"error": "Not found"}, status=status.HTTP_404_NOT_FOUND
        )
    order.status = "Rejection"
    order.save()
    return Response({"message": "Заказ отменён"}, status=status.HTTP_200_OK)


@api_view(["POST"])
def path_order(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(
            {"error": "Not found"}, status=status.HTTP_404_NOT_FOUND
        )
    order.status = "In path"
    order.save()
    return Response({"message": "Заказ отправлен"}, status=status.HTTP_200_OK)


@api_view(["POST"])
def deliver_order(request, pk):
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(
            {"error": "Not found"}, status=status.HTTP_404_NOT_FOUND
        )
    order.status = "Delivered"
    order.save()
    return Response({"message": "Заказ доставлен"}, status=status.HTTP_200_OK)
