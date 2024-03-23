from django.shortcuts import render
from django.views import View

from shop.service import CatalogService


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
