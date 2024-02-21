from django.contrib import admin

from .models import Classroom, Course, Grade, HomeWork, Roll, Subject


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "year",
    )


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "section",
        "year",
    )


@admin.register(Classroom)
class ClassAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "year",
        "course",
    )


@admin.register(Roll)
class RollAdmin(admin.ModelAdmin):
    list_display = (
        "course",
        "classroom",
        "student",
        "year",
    )


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "subject",
        "test_1",
        "test_2",
        "test_average",
        "exam",
        "section_average",
        "section",
        "year",
    )


@admin.register(HomeWork)
class HomeWorkAdmin(admin.ModelAdmin):
    list_display = (
        "teacher",
        "topic",
        "date_create",
        "date_close",
    )
