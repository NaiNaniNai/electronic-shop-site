from shop.repository import (
    IndexPageRepository,
    CatalogRepository,
    CompositeCategoryRepository,
    CategoryRepository,
)


class IndexPageService:
    """Service for view in index page"""

    def get_banner_product(self) -> dict:
        banner_products = IndexPageRepository.get_banner_info()
        return {
            "banner_products": banner_products,
        }

    def get_mobile_product(self) -> dict:
        mobile_products = IndexPageRepository.get_mobile_product()
        return {
            "mobile_products": mobile_products,
        }

    def get_watch_product(self) -> dict:
        watch_products = IndexPageRepository.get_watch_product()
        return {
            "watch_products": watch_products,
        }

    def get_laptop_product(self) -> dict:
        laptop_products = IndexPageRepository.get_laptop_product()
        return {
            "laptop_products": laptop_products,
        }


class CatalogService:
    """Service for view catalog page"""

    def __init__(self, request):
        self.request = request

    def get(self) -> dict:
        category_list = CatalogRepository.get_category_without_parent()
        return {
            "category_list": category_list,
        }


class CompositeCategoryService:
    """Service for view composite categories"""

    def __init__(self, request, slug):
        self.request = request
        self.slug = slug

    def get(self) -> dict:
        composite_category = CompositeCategoryRepository.get_category_by_slug(self.slug)
        children = CompositeCategoryRepository.get_children(composite_category)
        return {
            "composite_category": composite_category,
            "children": children,
        }


class CategoryService:
    """Service for view category and products this category"""

    def __init__(self, request, slug):
        self.request = (request,)
        self.slug = slug

    def get(self):
        category = CategoryRepository.get_by_slug(self.slug)
        products = CategoryRepository.get_products(category)
        return {
            "category": category,
            "products": products,
        }
