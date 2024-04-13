from django.urls import path

from .views import (
    orders_user,
    accept_order,
    rejection_order,
    path_order,
    deliver_order,
)

urlpatterns = [
    path("orders", orders_user),
    path("accept/<int:pk>", accept_order),
    path("rejection/<int:pk>", rejection_order),
    path("path/<int:pk>", path_order),
    path("deliver/<int:pk>", deliver_order),
]
