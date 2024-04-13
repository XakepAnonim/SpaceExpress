from django.urls import path

from .service import get_city_name
from .views import (
    get_order_handler,
    get_path,
    cancel_order,
    history_orders,
    make_order,
)

urlpatterns = [
    path("", get_order_handler),
    path("get_name/<int:pk>", get_city_name),
    path("get_path/<int:pk>", get_path),
    path("make/<int:pk>", make_order),
    path("cancel/<int:pk>", cancel_order),
    path("history", history_orders),
]
