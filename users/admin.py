from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserForm, UserRegistrationForm
from .models import CustomUser, Student, Teacher


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = UserRegistrationForm
    form = UserForm

    list_display = (
        "username",
        "is_active",
        "is_staff",
        "is_superuser",
        "date_join",
        "role",
    )
    fieldsets = (
        (
            "User",
            {
                "fields": ("username", "password"),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "role",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            "User",
            {
                "fields": ("username", "password1", "password2"),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "role",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "is_active",
        "is_staff",
        "is_superuser",
        "date_join",
        "role",
    )


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "is_active",
        "is_staff",
        "is_superuser",
        "date_join",
        "role",
    )
