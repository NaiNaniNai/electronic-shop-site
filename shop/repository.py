from django.db.models import QuerySet, Q

from shop.models import Product, Category


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


class CatalogRepository:
    """Class for interacting with category models"""

    @staticmethod
    def get_category_without_parent() -> QuerySet[Category]:
        return Category.objects.filter(parent=None)


class CompositeCategoryRepository:
    """Class for interacting with category models with parent"""

    @staticmethod
    def get_category_by_slug(slug: str) -> Category:
        return Category.objects.filter(Q(slug=slug) & Q(parent=None)).first()

    @staticmethod
    def get_children(category: Category):
        return Category.objects.filter(parent=category)


class CategoryRepository:
    """Class for interacting with models in category page"""

    @staticmethod
    def get_by_slug(slug: str) -> Category | None:
        category = Category.objects.filter(slug=slug).first()
        if category and category.parent:
            return category
        return None

    @staticmethod
    def get_products(category: Category) -> QuerySet[Product]:
        return Product.objects.filter(category=category)