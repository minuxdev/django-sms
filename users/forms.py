from django import forms
from django.contrib.auth.admin import UserChangeForm, UserCreationForm

from .models import CustomUser


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "password1",
            "password2",
            "role",
        )


class UserForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "role",
        )
