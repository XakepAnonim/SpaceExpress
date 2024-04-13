from rest_framework import status

from apps.company.serializers import OrdersUserSerializer

user_orders_response = {status.HTTP_200_OK: OrdersUserSerializer}
