from django.urls import path

from apps.products.views import (
    get_products_handler,
    create_product_handler,
    get_or_create_review_handler,
    delete_review_handler,
    manage_product_handler,
)

urlpatterns = [
    path("", get_products_handler),
    path("<int:pk>", manage_product_handler),
    path("add", create_product_handler),
    path("product/<int:product_pk>/comments", get_or_create_review_handler),
    path("comments/<int:pk>", delete_review_handler),
]
