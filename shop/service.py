from shop.repository import IndexPageRepository


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


class BannerSectionService:
    """Service for view in index page banner section"""
