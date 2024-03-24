from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from shop.service import (
    CatalogService,
    CompositeCategoryService,
    CategoryService,
    ProductService,
    UserCartService,
)


class IndexPageView(View):
    """View of main page"""

    def get(self, request):
        return render(request, "index_page.html")


class CatalogView(View):
    """View of catalog (Category) of product"""

    def get(self, request):
        service = CatalogService(request)
        context = service.get()
        return render(request, "catalog.html", context)


class CompositeCategoryView(View):
    """View of category with parent"""

    def get(self, request, slug):
        service = CompositeCategoryService(request, slug)
        context = service.get()
        return render(request, "composite_сategory.html", context)


class CategoryView(View):
    """View of products of the same category"""

    def get(self, request, slug):
        service = CategoryService(request, slug)
        context = service.get()
        return render(request, "category.html", context)


class ProductView(View):
    """Detail view of product"""

    def get(self, request, slug):
        service = ProductService(request, slug)
        context = service.get()
        return render(request, "product.html", context)


def add_to_cart(request, product_slug):
    if request.method == "GET":
        service = UserCartService(request, product_slug)
        service.get()
    return redirect(reverse("product", kwargs={"slug": product_slug}))
