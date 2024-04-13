from django.db import models

from ..products.models import Product
from ..users.models import User

STATUS = {
    ("Accepted", "Принят"),
    ("Rejection", "Отказ"),
    ("Processed", "Обрабатывается"),
    ("In path", "В пути"),
    ("Delivered", "Доставлен"),
}


class Order(models.Model):
    """
    Модель заказа
    """

    product = models.ManyToManyField(
        Product,
        related_name="order",
        verbose_name="Продукты",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )
    city_name = models.CharField(max_length=28, verbose_name="ПВЗ")
    delivery_path = models.CharField(
        max_length=55, verbose_name="Путь доставки"
    )
    status = models.CharField(
        max_length=12,
        choices=STATUS,
        default="Processed",
        verbose_name="Статус заказа",
    )
    rejection_reason = models.TextField(
        blank=True, verbose_name="Причина отказа"
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class HistoryOrder(models.Model):
    orders = models.ManyToManyField(
        Order,
        related_name="history_orders",
        verbose_name="Заказ",
    )

    class Meta:
        verbose_name = "История заказов"
        verbose_name_plural = "Истории заказов"
