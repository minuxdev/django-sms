from django import forms
from django.contrib.auth.admin import UserChangeForm, UserCreationForm

from .models import CustomUser, Profile, Student, Teacher


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


class StudentForm(UserRegistrationForm):
    class Meta(UserRegistrationForm.Meta):
        model = Student


class TeacherForm(UserRegistrationForm):
    class Meta(UserRegistrationForm.Meta):
        model = Teacher


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
        widgets = {
            "dob": forms.DateInput(attrs={"type": "date"}),
            "phone_no": forms.NumberInput(
                attrs={"minlength": 4, "maxlength": 9, "type": "number"}
            ),
            "parent_phone_no": forms.NumberInput(
                attrs={"minlength": 4, "maxlength": 9, "type": "number"}
            ),
        }
