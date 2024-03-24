from django.urls import path

from account import views

urlpatterns = [
    path("singin/", views.SinginView.as_view(), name="singin"),
    path("singup/", views.SingupView.as_view(), name="singup"),
    path("logout/", views.logout_view, name="logout"),
    path("confirm/<str:token>/", views.singup_confirm, name="confirm_singup"),
    path("reset_password/", views.ResetPasswordView.as_view(), name="reset_password"),
    path(
        "reset_password_confirm/<str:token>/",
        views.ConfirmRestPasswordView.as_view(),
        name="confirm_reset_password",
    ),
]
