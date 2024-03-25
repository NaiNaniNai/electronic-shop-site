from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    """Model of user"""

    slug = models.SlugField(max_length=128, unique=True, verbose_name="Слаг")
    email = models.EmailField(unique=True, verbose_name="Почта")
    phone = PhoneNumberField(verbose_name="Номер телефона")
    groups = models.ManyToManyField(
        "auth.Group", related_name="users", blank=True, verbose_name="Группы"
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission", related_name="users", blank=True, verbose_name="Права"
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.username}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.username
        super().save(*args, **kwargs)
