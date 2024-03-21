import uuid

from django.conf import settings
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.cache import cache

from account.repository import UserRepository
from account.tasks import send_email_task


class SendEmailService:
    """Service for send email in views"""

    def __init__(self, request):
        self.request = request


class SingupService:
    """Service for singup user in site"""

    def __init__(self, request, form):
        self.request = request
        self.form = form

    def post(self):
        username = self.form.cleaned_data.get("username")
        email = self.form.cleaned_data.get("email")
        password = self.form.cleaned_data.get("password1")
        token = self.get_token()
        self.caching(token, username, email, password)
        message = self.get_message(token)
        print(message)
        send_email_task.delay(message, email)

    def get_token(self) -> str:
        token = uuid.uuid4().hex
        return token

    def get_message(self, token):
        confirm_link = self.get_confirm_link(token)
        message = (
            f"Для подтверждения регистрации пройдите по ссылке\n"
            f"Подтвердить! \n {confirm_link}"
        )
        return message

    def get_confirm_link(self, token):
        current_site = get_current_site(self.request)
        return f"http://{current_site.domain}/accounts/confirm/{token}"

    def caching(self, token, username, email, password):
        redis_key = settings.USER_CONFIRMATION_KEY.format(token=token)
        value = {"username": username, "email": email, "password": password}
        cache.set(redis_key, value, timeout=settings.USER_CONFIRMATION_TIMEOUT)


class ConfirmSigupService:
    """Service for confirmation singup in site"""

    def __init__(self, request, token):
        self.request = request
        self.token = token

    def get(self):
        redis_key = settings.USER_CONFIRMATION_KEY.format(token=self.token)
        user_info = cache.get(redis_key)
        if not user_info:
            return self.get_context_data("error")
        username = user_info.get("username")
        email = user_info.get("email")
        password = user_info.get("password")
        UserRepository.create_user(username, email, password)
        cache.delete(redis_key)

    def get_context_data(self, message):
        if message == "error":
            return messages.error(
                self.request,
                "Не удалось закончить регистарцию акаунта! Возможно истёк срок ссылки",
            )
