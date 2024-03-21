from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

UserModel = get_user_model()


class SingupForm(UserCreationForm):
    """Form of singup user"""

    email = forms.EmailField(
        label="Электронная почта",
        error_messages={
            "unique": "Пользователь с такой почтой уже существует.",
            "invalid": "Введите корректный адрес электронной почты.",
        },
    )

    class Meta:
        model = UserModel
        fields = (
            "username",
            "email",
        )


class ConfirmResetPasswordForm(forms.ModelForm):
    """Form of confirm reset password user"""

    password = forms.CharField(
        label="lock", widget=forms.PasswordInput(attrs={"placeholder": "Новый пароль"})
    )
    repeated_password = forms.CharField(
        label="lock",
        widget=forms.PasswordInput(attrs={"placeholder": "Повторите пароль"}),
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        repeated_password = cleaned_data.get("repeated_password")

        if password and repeated_password and password != repeated_password:
            raise forms.ValidationError("Пароли не совпадают")

        return cleaned_data

    class Meta:
        model = UserModel
        fields = ("password", "repeated_password")
