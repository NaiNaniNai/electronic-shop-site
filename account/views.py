from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView

from account.forms import SingupForm
from account.service import SingupService, ConfirmSigupService


class SingupView(FormView):
    """View of registration in site"""

    form_class = SingupForm
    template_name = "singup.html"
    success_url = reverse_lazy("singup")

    def form_valid(self, form):
        service = SingupService(self.request, form)
        service.post()
        return super().form_valid(form)


def singup_confirm(request, token):
    """Confirm of singup user in site"""

    if request.method == "GET":
        service = ConfirmSigupService(request, token)
        service.get()
        return redirect(reverse("singin"))


class SinginView(FormView):
    form_class = AuthenticationForm
    template_name = "singin.html"
    success_url = reverse_lazy("singin")

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return redirect(self.get_success_url())
