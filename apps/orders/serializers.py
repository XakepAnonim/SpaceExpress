from rest_framework import serializers

from .models import Order, HistoryOrder
from ..products.serializers import ProductSerializer


class OrderSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Order
    """

    product = ProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "city_name", "delivery_path", "product", "status"]


class HistoryOrderSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True)

    class Meta:
        model = HistoryOrder
        fields = "__all__"
