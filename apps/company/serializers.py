from rest_framework import serializers

from .models import OrdersUser
from ..orders.serializers import OrderSerializer


class OrdersUserSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True)

    class Meta:
        model = OrdersUser
        fields = ["orders"]
