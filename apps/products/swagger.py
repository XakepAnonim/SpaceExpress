from drf_spectacular.utils import OpenApiResponse
from rest_framework import status

from apps.products.serializers import (
    DisplayProductSerializer,
    ProductSerializer,
    ReviewSerializer,
)

get_products_responses = {status.HTTP_200_OK: DisplayProductSerializer}

get_product_responses = {status.HTTP_200_OK: ProductSerializer}

create_product_responses = {
    status.HTTP_200_OK: ProductSerializer,
    status.HTTP_400_BAD_REQUEST: OpenApiResponse(
        description='{"<Название поля>": ["Обязательное поле."],}'
    ),
}

update_product_responses = {
    status.HTTP_200_OK: ProductSerializer,
    status.HTTP_400_BAD_REQUEST: OpenApiResponse(
        description='{"<Название поля>": ["Обязательное поле."],}'
    ),
}

get_product_review_response = {status.HTTP_200_OK: ReviewSerializer}

create_product_review_response = {status.HTTP_200_OK: ReviewSerializer}

delete_product_review_response = {
    status.HTTP_204_NO_CONTENT: OpenApiResponse(description=""),
    status.HTTP_403_FORBIDDEN: OpenApiResponse(
        description='{"detail": "У вас недостаточно прав '
        'для выполнения данного действия."}'
    ),
    status.HTTP_404_NOT_FOUND: OpenApiResponse(
        description='{"Detail": "Страница не найдена."}'
    ),
}
