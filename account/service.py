import uuid

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.cache import cache

from account.repository import UserRepository
from account.tasks import send_email_task


def get_token() -> str:
    token = uuid.uuid4().hex

    return token


class SingupService:
    """Service for singup user in site"""

    def __init__(self, request, form):
        self.request = request
        self.form = form

    def post(self) -> None:
        username = self.form.cleaned_data.get("username")
        email = self.form.cleaned_data.get("email")
        password = self.form.cleaned_data.get("password1")
        token = get_token()
        self.caching(token, username, email, password)
        title = "Подтвердите регистрацию"
        message = self.get_message(token)
        send_email_task.delay(title, message, email)
        messages.success(
            self.request,
            "На вашу почту отправлено письмо! Следуйте инструкции для завершения регистрации.",
        )

    def get_message(self, token) -> str:
        confirm_link = self.get_confirm_link(token)
        message = f"Для подтверждения регистрации пройдите по ссылке\n Подтвердить! {confirm_link}"

        return message

    def get_confirm_link(self, token) -> str:
        current_site = get_current_site(self.request)

        return f"http://{current_site.domain}/accounts/confirm/{token}"

    def caching(self, token, username, email, password) -> None:
        redis_key = settings.USER_CONFIRMATION_KEY.format(token=token)
        value = {"username": username, "email": email, "password": password}
        cache.set(redis_key, value, timeout=settings.USER_CONFIRMATION_TIMEOUT)


class ConfirmSigupService:
    """Service for confirmation singup in site"""

    def __init__(self, request, token):
        self.request = request
        self.token = token

    def get(self) -> dict | None:
        redis_key = settings.USER_CONFIRMATION_KEY.format(token=self.token)
        user_info = cache.get(redis_key)

        if not user_info:
            return self.get_context_data()

        username = user_info.get("username")
        email = user_info.get("email")
        password = user_info.get("password")
        UserRepository.create_user(username, email, password)
        cache.delete(redis_key)
        return None

    def get_context_data(self) -> dict:
        messages.error(
            self.request,
            "Не удалось закончить регистарцию акаунта! Возможно истёк срок ссылки",
        )

        return {"Error": "True"}


class ResetPasswordService:
    """Service for reset user password"""

    def __init__(self, request, form):
        self.request = request
        self.form = form

    def post(self) -> dict | None:
        email = self.form.cleaned_data.get("email")
        user = UserRepository.get_by_email(email)

        if not user:
            return self.get_context_data()

        token = get_token()
        self.caching(token, user)
        title = "Сброс пароля"
        message = self.get_message(token)
        send_email_task.delay(title, message, email)
        messages.success(
            self.request,
            "На вашу почту отправлено письмо! Следуйте инструкции для завершения сброса пароля.",
        )
        return None

    def get_message(self, token) -> str:
        confirm_link = self.get_confirm_link(token)
        message = f"Для сброса пароля перейдите по ссылке\nПерейти! \n{confirm_link}"

        return message

    def get_confirm_link(self, token):
        current_site = get_current_site(self.request)

        return f"http://{current_site.domain}/accounts/reset_password_confirm/{token}"

    def caching(self, token, user):
        redis_key = settings.USER_CONFIRMATION_KEY.format(token=token)
        value = {"user": user}
        cache.set(redis_key, value, timeout=settings.USER_CONFIRMATION_TIMEOUT)

    def get_context_data(self) -> dict:
        messages.error(
            self.request,
            "Пользователя с такой почтой не существует!",
        )

        return {"Error": "True"}


class ConfirmResetPasswordService:
    """Service for confirm reset user password"""

    def __init__(self, request, form, token):
        self.request = request
        self.form = form
        self.token = token

    def get(self) -> dict:
        return {
            "form": self.form,
        }

    def post(self) -> dict | None:
        redis_key = settings.USER_CONFIRMATION_KEY.format(token=self.token)
        user = self.get_user_by_redis_key(redis_key)

        if not user:
            return self.get_context_data()

        self.change_password(user)
        cache.delete(redis_key)
        return None

    def get_user_by_redis_key(self, redis_key) -> None | User:
        user_info = cache.get(redis_key)

        if not user_info:
            return None

        user = user_info.get("user")

        return user

    def get_context_data(self) -> dict:
        messages.error(
            self.request,
            "Не удалось сбросить пароль от акаунта! Возможно истёк срок ссылки",
        )

        return {"Error": "True"}

    def change_password(self, user) -> None:
        new_password = self.form.cleaned_data.get("password")
        UserRepository.change_password(user, new_password)
