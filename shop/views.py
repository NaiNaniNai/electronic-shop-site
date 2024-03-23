from django.shortcuts import render
from django.views import View

from shop.service import CatalogService, CompositeCategoryService


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
