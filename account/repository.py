from django.contrib.auth import get_user_model

from account.models import CustomUser


class UserRepository:
    """Class for interacting with the user model"""

    @staticmethod
    def get_by_email(email):
        return get_user_model().objects.get(email=email)

    @staticmethod
    def create_user(username, email, password):
        CustomUser.objects.create_user(
            username=username, email=email, password=password
        )
