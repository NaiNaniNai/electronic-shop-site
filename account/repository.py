from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

from account.models import CustomUser


class UserRepository:
    """Class for interacting with the user model"""

    @staticmethod
    def get_by_email(email: str) -> User:
        return CustomUser.objects.filter(email=email).first()

    @staticmethod
    def create_user(username: str, email: str, password: str) -> None:
        CustomUser.objects.create_user(
            username=username, email=email, password=password
        )

    @staticmethod
    def change_password(user: User, new_password: str) -> None:
        user.set_password(new_password)
        user.save()

    @staticmethod
    def get_from_request(request) -> User:
        return request.user

    @staticmethod
    def get_by_slug(slug: str) -> CustomUser:
        return CustomUser.objects.filter(slug=slug).first()

    @staticmethod
    def edit_profile(
        user: CustomUser, last_name: str, first_name: str, phone: PhoneNumberField
    ) -> None:
        if not last_name:
            last_name = user.last_name
        if not first_name:
            first_name = user.first_name
        if not phone:
            phone = user.phone

        user.last_name = last_name
        user.first_name = first_name
        user.phone = phone
        user.save()
