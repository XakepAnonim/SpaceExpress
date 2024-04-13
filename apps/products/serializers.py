from rest_framework import serializers

from ..main.serializers import ManufacturerSerializer
from ..products.models import Product, Review, Category
from ..users.models import User


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Product
    """

    class Meta:
        model = Product
        fields = "__all__"


class DisplayProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Product
    """

    company = ManufacturerSerializer()

    class Meta:
        model = Product
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Category
    """

    class Meta:
        model = Category
        fields = "__all__"


class AuthorSerializer(serializers.ModelSerializer):
    """
    Сериализатор для получения автора отзыва
    """

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name"]


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор для получения отзывов
    """

    author = AuthorSerializer()

    class Meta:
        model = Review
        fields = "__all__"


class CreateReviewSerializer(serializers.ModelSerializer):
    product = serializers.IntegerField(required=False)
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = "__all__"

    def validate(self, data):
        text = data.get("text")

        if not any([text]):
            raise serializers.ValidationError("Заполните поле: 'text'")

        return data
