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
    path("category/<str:slug>/", views.CategoryView.as_view(), name="category"),
    path("product/<str:slug>/", views.ProductView.as_view(), name="product"),
    path(
        "product/<str:product_slug>/add_to_cart/", views.add_to_cart, name="add_to_cart"
    ),
]
