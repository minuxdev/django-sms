from django.contrib import admin

from .models import (
    Classroom,
    Course,
    Grade,
    HomeWork,
    Parent,
    Roll,
    Section,
    Subject,
    TeacherContract,
)


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
        "subject",
        "topic",
        "date_create",
        "date_close",
    )


@admin.register(TeacherContract)
class TeacherContractAdmin(admin.ModelAdmin):
    list_display = (
        "teacher",
        "category",
        "status",
        "date_celebrate",
        "date_start",
        "date_end",
    )


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ("user", "full_name", "address")


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
