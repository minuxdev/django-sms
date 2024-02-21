from django.urls import path

from . import views

app_name = "sms"

urlpatterns = [
    # LIST
    path("", views.RollView.as_view(), name="list_student"),
    path("dashboard/", views.RollView.as_view(), name="dashboard"),
    path("courses/", views.CourseView.as_view(), name="list_course"),
    path("classroom/", views.ClassroomView.as_view(), name="list_classroom"),
    path("grades/", views.GradeView.as_view(), name="list_grade"),
    path("teachers/", views.TeacherView.as_view(), name="list_teacher"),
    path("home-works/", views.HomeWrokView.as_view(), name="list_homework"),
    # DETAILS
    path(
        "roll/<pk>/detail/",
        views.RollDetailView.as_view(),
        name="detail_student",
    ),
    path(
        "teacher/<pk>/detail/",
        views.TeacherDetailView.as_view(),
        name="detail_teacher",
    ),
    path(
        "class/<pk>/detail/",
        views.ClassroomDetailView.as_view(),
        name="detail_classroom",
    ),
    path(
        "course/<pk>/detail/",
        views.CourseDetailView.as_view(),
        name="detail_course",
    ),
    path(
        "grade/<pk>/detail/",
        views.GradeDetailView.as_view(),
        name="detail_grade",
    ),
    path(
        "home-work/<pk>/detail/",
        views.HomeWrokDetailView.as_view(),
        name="detail_homework",
    ),
]
