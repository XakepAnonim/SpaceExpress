from django.db import models
from django.utils import timezone

from ..main.models import Manufacturer
from ..users.models import User

STATUS = {("In stock", "В наличии"), ("Out of stock", "Нет в наличии")}


class Product(models.Model):
    """
    Модель продукта
    """

    name = models.CharField(max_length=128, verbose_name="Название продукта")
    description = models.TextField(
        max_length=256, verbose_name="Описание продукта"
    )
    size = models.CharField(max_length=10, verbose_name="Размер продукта")
    weight = models.PositiveIntegerField(verbose_name="Вес продукта (кг)")
    price = models.DecimalField(
        max_digits=9, decimal_places=2, verbose_name="Цена продукта"
    )
    status = models.CharField(
        max_length=25, choices=STATUS, verbose_name="Статус продукта"
    )
    quantity = models.PositiveIntegerField(
        verbose_name="Количество"
    )

    product_photo = models.ImageField(
        upload_to="product_photos",
        verbose_name="Фото продукта",
        null=True,
        blank=True,
    )
    category = models.ManyToManyField(
        "Category",
        related_name="product",
        verbose_name="Категория",
        blank=True,
    )
    company = models.ForeignKey(
        Manufacturer,
        on_delete=models.CASCADE,
        related_name="product",
        verbose_name="Кому принадлежит продукт",
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.quantity == 0:
            self.status = "Out of stock"
        elif self.quantity > 0:
            self.status = "In stock"
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["id"]


class Category(models.Model):
    """
    Модель категории
    """

    name = models.CharField(max_length=128, verbose_name="Название категории")
    description = models.TextField(
        max_length=256, verbose_name="Описание категории", blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Review(models.Model):
    """
    Модель для Отзывов
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="review",
        verbose_name="Продукт",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        related_name="reviews_author",
    )
    text = models.TextField(blank=True, null=True, verbose_name="Текст")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.author} - {self.created_at}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["-created_at"]
