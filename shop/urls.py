from django.urls import path

from shop import views

urlpatterns = [
    path("", views.IndexPageView.as_view(), name="index"),
]
