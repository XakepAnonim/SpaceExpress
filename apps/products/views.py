from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product, Review
from .serializers import (
    ProductSerializer,
    DisplayProductSerializer,
    ReviewSerializer,
    CreateReviewSerializer,
)
from .swagger import (
    get_products_responses,
    get_product_responses,
    create_product_responses,
    get_product_review_response,
    create_product_review_response,
    update_product_responses, delete_product_review_response,
)


@extend_schema_view(
    get=extend_schema(
        responses=get_products_responses,
        request=DisplayProductSerializer,
        tags=["Product"],
    )
)
@api_view(["GET"])
def get_products_handler(request):
    """
    Обработчик получения всех продуктов
    """
    products = Product.objects.all()
    serializer = DisplayProductSerializer(products, many=True)
    return Response({"products": serializer.data}, status=status.HTTP_200_OK)


def get_product_handler(request, product):
    serializer = ProductSerializer(product)
    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema_view(
    post=extend_schema(
        responses=create_product_responses,
        request=ProductSerializer,
        tags=["Product"],
    )
)
@api_view(["POST"])
def create_product_handler(request):
    """
    Обработчик создания продукта
    """
    if not request.user.is_authenticated or not request.user.is_manufacturer:
        return Response(
            {"error": {"message": "Forbidden for you"}},
            status=status.HTTP_403_FORBIDDEN,
        )

    request.data["company"] = request.user.company.pk
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"data": f"Продукт '{serializer.data}' добавлен"})
    return Response(
        {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
    )


def update_product_handler(request, product):
    """
    Обработчик обновления продукта
    """

    serializer = ProductSerializer(
        data=request.data, instance=product, partial=True
    )
    if serializer.is_valid():
        serializer.save()
        return Response({"data": f"Продукт '{serializer.data}' обновлен"})
    return Response(
        {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
    )


@extend_schema_view(
    get=extend_schema(
        responses=get_product_responses,
        request=ProductSerializer,
        tags=["Product"],
    ),
    patch=extend_schema(
        responses=update_product_responses,
        request=ProductSerializer,
        tags=["Product"],
    ),
)
@api_view(["GET", "PATCH"])
def manage_product_handler(request, pk):
    try:
        product = get_object_or_404(Product, pk=pk)
    except Product.DoesNotExist:
        return Response(
            {"error": "Not found"}, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "GET":
        return get_product_handler(request, product)
    if request.method == "PATCH":
        return update_product_handler(request, product)


def get_product_reviews_handler(product):
    """
    Обработчик для получения отзывов продукта
    """
    reviews = Review.objects.filter(product=product)
    serializer = ReviewSerializer(reviews, many=True)

    return Response(
        serializer.data,
        status=status.HTTP_200_OK,
    )


def create_review_handler(request, product):
    """
    Обработчик для создания отзыва
    """
    serializer = CreateReviewSerializer(
        data=request.data, context={"request": request}
    )

    if serializer.is_valid(raise_exception=True):
        review = serializer.save(author=request.user, product=product)
        response_serializer = ReviewSerializer(review)
        return Response(
            response_serializer.data, status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema_view(
    get=extend_schema(
        responses=get_product_review_response,
        request=ReviewSerializer,
        tags=["Review"],
    ),
    post=extend_schema(
        responses=create_product_review_response,
        request=ReviewSerializer,
        tags=["Review"],
    ),
)
@api_view(["POST", "GET"])
def get_or_create_review_handler(request, product_pk):
    """
    Обработчик для создания/получения отзывов
    """
    product = get_object_or_404(Product, pk=product_pk)

    if request.method == "POST":
        return create_review_handler(request, product)
    if request.method == "GET":
        return get_product_reviews_handler(product)


@extend_schema(
    responses=delete_product_review_response,
    tags=["Product"]
)
@api_view(["DELETE"])
def delete_review_handler(request, pk):
    """
    Обработчик для удаления отзыва
    """
    review = get_object_or_404(Review, pk=pk)
    if request.user.id != review.author.id:
        return Response(
            {
                "error": {
                    "code": status.HTTP_403_FORBIDDEN,
                    "message": "Forbidden",
                }
            },
            status=status.HTTP_403_FORBIDDEN,
        )
    review.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
