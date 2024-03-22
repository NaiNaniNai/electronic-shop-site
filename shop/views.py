from django.shortcuts import render
from django.views import View


class IndexPageView(View):
    """View of main page"""

    def get(self, request):
        return render(request, "index_page.html")
