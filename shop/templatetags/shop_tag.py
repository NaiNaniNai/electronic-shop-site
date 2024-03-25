from django import template

from shop.service import IndexPageService

register = template.Library()


@register.inclusion_tag("tags/banner_section.html")
def get_banner_section() -> dict:
    """Output banner section in index page"""

    service = IndexPageService()
    context = service.get_banner_product()

    return context


@register.inclusion_tag("tags/mobile_section.html")
def get_mobile_section() -> dict:
    """Output mobile section product in index page"""

    service = IndexPageService()
    context = service.get_mobile_product()

    return context


@register.inclusion_tag("tags/watch_section.html")
def get_watch_section() -> dict:
    """Output watch section product in index page"""

    service = IndexPageService()
    context = service.get_watch_product()

    return context


@register.inclusion_tag("tags/laptop_section.html")
def get_laptop_section() -> dict:
    """Output laptop section product in index page"""

    service = IndexPageService()
    context = service.get_laptop_product()

    return context


@register.inclusion_tag("tags/discount_product_section.html")
def get_discount_product_section() -> dict:
    service = IndexPageService()
    context = service.get_discount_product()

    return context
