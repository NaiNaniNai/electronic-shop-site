from django.urls import path

from account import views

urlpatterns = [
    path("singup/", views.SingupView.as_view(), name="singup"),
    path("singin/", views.SinginView.as_view(), name="singin"),
    path("confirm/<str:token>/", views.singup_confirm, name="confirm_singup"),
]
