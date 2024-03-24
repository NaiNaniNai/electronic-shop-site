from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from shop.choices import CHARACTERISTICS, COLOR

User = get_user_model()
PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]


class Category(models.Model):
    """Model of category"""

    name = models.CharField(max_length=128, verbose_name="Название")
    slug = models.SlugField(max_length=128, verbose_name="Слаг")
    parent = models.ForeignKey(
        "self",
        verbose_name="Родитель",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    image = models.ImageField(
        upload_to="category/", blank=True, null=True, verbose_name="Фотография"
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return f"{self.name} {self.slug}"


class Characteristic(models.Model):
    """Class of characteristics"""

    name = models.CharField(
        max_length=128, choices=CHARACTERISTICS, verbose_name="Название"
    )
    value = models.CharField(max_length=128, verbose_name="Значение")

    class Meta:
        verbose_name = "Характеристика"
        verbose_name_plural = "Характеристики"

    def __str__(self):
        return f"{self.name} {self.value}"


class Product(models.Model):
    """Model of product"""

    name = models.CharField(max_length=128, verbose_name="Название")
    slug = models.SlugField(max_length=128, verbose_name="Слаг")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категория",
    )
    color = models.CharField(max_length=128, choices=COLOR, verbose_name="Цвет")
    characteristics = models.ManyToManyField(
        Characteristic, related_name="exercises", verbose_name="Характеристики"
    )
    price = models.PositiveIntegerField(verbose_name="Цена")
    discount = models.DecimalField(
        max_digits=3,
        decimal_places=0,
        default=Decimal(0),
        validators=PERCENTAGE_VALIDATOR,
    )
    discount_price = models.PositiveIntegerField(
        blank=True, null=True, verbose_name="Цена по скидке"
    )
    image = models.ImageField(
        upload_to="product/", blank=True, null=True, verbose_name="Фотография"
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.name} {self.color} {self.price}"

    def save(self, *args, **kwargs):
        if self.discount > 0:
            self.discount_price = int(self.price * (100 - self.discount) / 100)
        else:
            self.discount_price = None
        super().save(*args, **kwargs)


class UserCart(models.Model):
    """Model of user's cart"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="cart", verbose_name="Пользователь"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="cart", verbose_name="Товар"
    )
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
    sum = models.PositiveIntegerField(
        blank=True, null=True, default=0, verbose_name="Сумма заказа"
    )

    class Meta:
        verbose_name = "Корзина пользователя"
        verbose_name_plural = "Корзины пользователей"

    def __str__(self):
        return f"{self.user} {self.product.name} {self.quantity}"

    def save(self, *args, **kwargs):
        if self.product.discount:
            self.sum = self.product.discount_price * self.quantity
        else:
            self.sum = self.product.price * self.quantity
        super().save(*args, **kwargs)
