from drf_spectacular.utils import OpenApiRequest, OpenApiExample
from rest_framework import status

from apps.orders.serializers import OrderSerializer, HistoryOrderSerializer

get_order_response = {status.HTTP_200_OK: OrderSerializer}

get_city_name_response = {
    status.HTTP_200_OK: "Название города с пвз занесён в заказ"
}

get_city_name_request = OpenApiRequest(
    request={
        "type": "object",
    },
    examples=[
        OpenApiExample(
            "JSON получения имени города",
            value={
                "city_name": "string",
            },
        )
    ],
)

get_history_order_response = {status.HTTP_200_OK: HistoryOrderSerializer}

get_path_request = OpenApiRequest(
    request={
        "type": "object",
    },
)

cancel_order_response = {
    status.HTTP_200_OK: "Заказ отменён"
}

cancel_order_request = OpenApiRequest(
    request={
        "type": "object",
    },
    examples=[
        OpenApiExample(
            "JSON отмены заказа",
            value={
                "text": "string",
            },
        )
    ],
)