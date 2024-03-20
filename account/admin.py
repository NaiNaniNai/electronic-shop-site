from django.contrib import admin

from account.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """Model of Custom User in admin panel"""

    list_display = ("id", "username", "email")
    list_display_links = ("username",)
