from django.urls import path

from shop import views

urlpatterns = [
    path("", views.IndexPageView.as_view(), name="index"),
    path("catalog/", views.CatalogView.as_view(), name="catalog"),
    path(
        "composite_category/<str:slug>/",
        views.CompositeCategoryView.as_view(),
        name="composite_category",
    ),
]
