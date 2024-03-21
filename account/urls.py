from django.urls import path

from account import views

urlpatterns = [
    path("test/", views.SingupView.as_view(), name="singup"),
    path("confirm/<str:token>/", views.singup_confirm, name="confirm_singup"),
]
