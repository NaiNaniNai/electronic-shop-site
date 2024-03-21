from django.contrib.auth.models import User

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
