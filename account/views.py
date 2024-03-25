from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import FormView

from account.forms import SingupForm, ConfirmResetPasswordForm
from account.service import (
    SingupService,
    ConfirmSigupService,
    ResetPasswordService,
    ConfirmResetPasswordService,
    ProfileService,
)


class SingupView(FormView):
    """View of registration in site"""

    form_class = SingupForm
    template_name = "singup.html"
    success_url = reverse_lazy("singin")

    def form_valid(self, form):
        service = SingupService(self.request, form)
        service.post()
        return super().form_valid(form)


def singup_confirm(request, token):
    """Confirm of singup user in site"""

    if request.method == "GET":
        service = ConfirmSigupService(request, token)
        context = service.get()
        if context:
            return redirect(reverse("singup"))
        return redirect(reverse("singin"))


class SinginView(FormView):
    """View of login in site"""

    form_class = AuthenticationForm
    template_name = "singin.html"
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return redirect(self.get_success_url())


class ResetPasswordView(FormView):
    """View of user reset password"""

    form_class = PasswordResetForm
    template_name = "reset_password.html"
    success_url = reverse_lazy("reset_password")

    def form_valid(self, form):
        service = ResetPasswordService(self.request, form)
        context = service.post()
        if context:
            return render(self.request, "reset_password.html", context)
        return super().form_valid(form)


class ConfirmRestPasswordView(View):
    """View of confirm reset password user"""

    def get(self, request, token):
        form = ConfirmResetPasswordForm
        service = ConfirmResetPasswordService(request, form, token)
        context = service.get()
        return render(request, "confirm_reset_password.html", context)

    def post(self, request, token):
        form = ConfirmResetPasswordForm(request.POST)
        if form.is_valid():
            service = ConfirmResetPasswordService(request, form, token)
            context = service.post()
            if context:
                return redirect(reverse("reset_password"))
            return redirect(reverse("singin"))
        messages.error(request, "Пароли не совпадают!")
        return redirect(reverse("confirm_reset_password", kwargs={"token": token}))


def logout_view(request):
    """Logout from site"""

    logout(request)
    return redirect(reverse("singin"))


class ProfileView(View):
    """View of user profile"""

    def get(self, request, profile_slug):
        service = ProfileService(request, profile_slug)
        context = service.get()
        return render(request, "profile.html", context)
