from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not password:
            raise ValueError("Password is required!")

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, password, **extra_fields)


class ROLE(models.TextChoices):
    ADMIN = "ADMIN", "Admin"
    TEACHER = "TEACHER", "Teacher"
    STUDENT = "STUDENT", "Student"
    STAFF = "STAFF", "Staff"


class CustomUser(AbstractBaseUser, PermissionsMixin):
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    username = models.CharField(max_length=50, unique=True)
    date_join = models.DateField(auto_now_add=True)
    role = models.CharField(max_length=10, choices=ROLE.choices)

    USERNAME_FIELD = "username"
    objects = UserManager()

    default_role = ROLE.ADMIN

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.default_role

        return super().save(*args, **kwargs)


class TeacherManager(models.Manager):
    def get_queryset(self, **kwargs):
        return super().get_queryset(**kwargs).filter(role=ROLE.TEACHER)


class StudentManager(models.Manager):
    def get_queryset(self, **kwargs):
        return super().get_queryset(**kwargs).filter(role=ROLE.STUDENT)


class Teacher(CustomUser):
    default_role = ROLE.TEACHER
    objects = TeacherManager()

    class Meta:
        proxy = True


class Student(CustomUser):
    default_role = ROLE.STUDENT
    objects = StudentManager()

    class Meta:
        proxy = True


class Profile(models.Model):
    user = models.OneToOneField(to=CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    phone_no = models.PositiveIntegerField(null=True, blank=True)
    guardian_name = models.PositiveIntegerField(null=True, blank=True)
    guardian_phone_no = models.CharField(max_length=9, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.first_name)
