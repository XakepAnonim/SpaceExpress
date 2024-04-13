from django.db import models

from ..orders.models import Order
from ..users.models import User


class OrdersUser(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )
    orders = models.ManyToManyField(
        Order,
        related_name="user_orders",
        verbose_name="Заказ",
    )

    class Meta:
        verbose_name = "Текущий заказ пользователя"
        verbose_name_plural = "Текущие заказы пользователей"
