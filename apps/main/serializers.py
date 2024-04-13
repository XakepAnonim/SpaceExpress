from rest_framework import serializers

from .models import Manufacturer, City


class ManufacturerSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Manufacturer
    """

    class Meta:
        model = Manufacturer
        fields = "__all__"


class CitySerializer(serializers.ModelSerializer):
    """
    Сериализатор модели City
    """

    class Meta:
        model = City
        fields = "__all__"
