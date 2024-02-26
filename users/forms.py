from django import forms
from django.contrib.auth.admin import UserChangeForm, UserCreationForm

from .models import CustomUser, Profile


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


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ("id",)
        widgets = {
            "dob": forms.DateInput(attrs={"type": "date"}),
            "phone_no": forms.NumberInput(
                attrs={"minlength": 4, "maxlength": 9, "type": "number"}
            ),
            "guardian_phone_no": forms.NumberInput(
                attrs={"minlength": 4, "maxlength": 9, "type": "number"}
            ),
        }
