from django.contrib.auth.models import User
from django.db.models import QuerySet, Q

from shop.models import Product, Category, UserCart


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


class ProductRepository:
    """Class for interacting with product model"""

    @staticmethod
    def get_by_slug(slug: str) -> Product:
        return Product.objects.filter(slug=slug).first()

    @staticmethod
    def get_by_id(id: int) -> Product:
        return Product.objects.filter(id=id).first()


class UserCartRepository:
    """Class for interacting with models in user's cart"""

    @staticmethod
    def get_by_product(user: User, product: Product) -> UserCart:
        return UserCart.objects.filter(user=user, product=product).first()

    @staticmethod
    def create_user_cart(user: User, product: Product) -> None:
        UserCart.objects.create(user=user, product=product, quantity=1)

    @staticmethod
    def increase_count_of_product(user: User, product: Product) -> None:
        cart = UserCartRepository.get_by_product(user, product)
        cart.quantity += 1
        cart.save()

    @staticmethod
    def get_carts(user: User) -> QuerySet[UserCart]:
        return UserCart.objects.filter(user=user).order_by("id")

    @staticmethod
    def reduce_count_of_product(cart: UserCart) -> None:
        if cart.quantity == 1:
            cart.delete()
        else:
            cart.quantity -= 1
            cart.save()


class DiscountProductRepository:
    """Class for interacting with product model with discount"""

    @staticmethod
    def get_product() -> QuerySet[Product]:
        return Product.objects.filter(discount_price__gte=1)
