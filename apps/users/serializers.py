from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import User, Application
from ..main.serializers import CitySerializer


class LogSerializer(serializers.Serializer):
    """
    Сериализатор для входа пользователя
    """

    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        if email and password:
            user = authenticate(email=email, password=password)
        attrs["user"] = user
        return attrs


class RegSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации пользователя
    """

    password = serializers.CharField(min_length=8)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "first_name",
            "last_name",
        ]

    def save(self, **kwargs):
        """
        Метод для сохранения нового пользователя.
        """
        user = User()
        user.email = self.validated_data["email"]
        user.first_name = self.validated_data["first_name"]
        user.last_name = self.validated_data["last_name"]
        user.is_manufacturer = self.validated_data.get(
            "is_manufacturer", False
        )
        user.set_password(self.validated_data["password"])
        user.save()
        return user


class ApplicationSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Application
    """

    class Meta:
        model = Application
        fields = "__all__"


class CityApplicationSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Application
    """

    cities = CitySerializer(many=True, read_only=True)

    class Meta:
        model = Application
        fields = "__all__"
