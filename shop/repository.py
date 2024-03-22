from django.db.models import QuerySet, Q

from shop.models import Product


class IndexPageRepository:
    """Class for interacting with models in index page"""

    @staticmethod
    def get_banner_info() -> QuerySet[Product]:
        return Product.objects.filter(
            Q(category__slug="phone") | Q(category__slug="watch")
        ).distinct("category")

    @staticmethod
    def get_mobile_product() -> QuerySet[Product]:
        return Product.objects.filter(category__slug="phone")[:4]

    @staticmethod
    def get_watch_product() -> QuerySet[Product]:
        return Product.objects.filter(category__slug="watch")[:4]

    @staticmethod
    def get_laptop_product() -> QuerySet[Product]:
        return Product.objects.filter(category__slug="laptop")[:4]
