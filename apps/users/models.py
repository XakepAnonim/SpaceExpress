from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from ..main.models import City


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, name, email=None, password=None, **extra_fields):
        """
        Метод для создания обычного пользователя.
        """
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(name, email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Модель пользователя
    """

    is_manufacturer = models.BooleanField(
        verbose_name="Компания производитель?", default=False
    )
    email = models.EmailField(verbose_name="Почта", unique=True)

    company = models.OneToOneField(
        "main.Manufacturer",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="users",
        verbose_name="Компания пользователя",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
    objects = UserManager()
    username = None

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Покупатель"
        verbose_name_plural = "Покупатели"
        ordering = ["id"]


class Application(models.Model):
    """
    Модель заявки
    """

    name = models.CharField(max_length=55, verbose_name="Название компании")
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="applications",
        verbose_name="Чья заявка",
    )
    cities = models.ManyToManyField(City, verbose_name="Города компании")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"
