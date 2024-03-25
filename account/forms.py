from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField

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


class EditProfileForm(forms.ModelForm):
    """For of edit profile user"""

    last_name = forms.CharField(label="Фамилия", required=False)
    first_name = forms.CharField(label="Имя", required=False)
    phone = PhoneNumberField(label="Номер телефона", required=False)

    class Meta:
        model = UserModel
        fields = (
            "last_name",
            "first_name",
            "phone",
        )
