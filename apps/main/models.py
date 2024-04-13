from django.db import models


class Manufacturer(models.Model):
    """
    Модель компании производителя
    """

    name = models.CharField(max_length=55, verbose_name="Название компании")
    user = models.OneToOneField(
        "users.User",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="manufacturer",
        verbose_name="Кому принадлежит компания",
    )
    cities = models.ManyToManyField(
        "City", verbose_name="Города компании"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Компания производитель"
        verbose_name_plural = "Компании производители"
        ordering = ["id"]


class City(models.Model):
    """
    Модель населённого пункта
    """

    name = models.CharField(
        max_length=55, verbose_name="Название населённого пункта"
    )
    coords = models.TextField(verbose_name="Координаты")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Населённый пункт"
        verbose_name_plural = "Населённые пункты"


class Warehouse(models.Model):
    """
    Модель склада компании
    """

    city = models.ForeignKey(
        City,
        on_delete=models.DO_NOTHING,
        related_name="warehouses",
        verbose_name="Населённый пункт",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.city.name

    class Meta:
        verbose_name = "Склад компании"
        verbose_name_plural = "Склады компаний"
