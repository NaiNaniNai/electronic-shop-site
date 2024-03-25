from django.contrib import admin

from shop.models import Category, Characteristic, Product, UserCart


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Model of category in admin panel"""

    list_display = ("name", "parent")
    list_display_links = ("name",)
    ordering = ("id",)

    prepopulated_fields = {"slug": ("name",)}


@admin.register(Characteristic)
class CharacteristicAdmin(admin.ModelAdmin):
    """Model of characteristic in admin panel"""

    list_display = ("name", "value")
    list_display_links = ("name",)
    ordering = ("id",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Model of product in admin panel"""

    list_display = (
        "name",
        "color",
        "price",
    )
    list_display_links = ("name",)
    list_filter = ("category",)
    search_fields = ("name", "category__name")
    ordering = ("id",)

    prepopulated_fields = {"slug": ("name",)}


@admin.register(UserCart)
class UserCartAdmin(admin.ModelAdmin):
    """Model of user's cart in admin panel"""

    list_display = ("user", "product", "quantity", "sum")
    list_display_links = ("user", "product")
    list_filter = ("user",)
    search_fields = ("user",)
    ordering = ("id",)
