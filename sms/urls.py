from django.urls import path

from . import views

app_name = "sms"

urlpatterns = [
    # LIST
    path("", views.RollView.as_view(), name="list_student"),
    path("dashboard/", views.RollView.as_view(), name="dashboard"),
    path("courses/", views.CourseView.as_view(), name="list_course"),
    path("subjects/", views.SubjectView.as_view(), name="list_subject"),
    path("classrooms/", views.ClassroomView.as_view(), name="list_classroom"),
    path("grades/", views.GradeView.as_view(), name="list_grade"),
    path("teachers/", views.TeacherView.as_view(), name="list_teacher"),
    path("home-works/", views.HomeWrokView.as_view(), name="list_homework"),
    # CREATE
    path("add/roll/", views.RollCreateView.as_view(), name="add_roll"),
    path("add/course/", views.CourseCreateView.as_view(), name="add_course"),
    path("add/grade/", views.GradeCreateView.as_view(), name="add_grade"),
    path(
        "add/subject/", views.SubjectCreateView.as_view(), name="add_subject"
    ),
    path(
        "add/classroom/",
        views.ClassroomCreateView.as_view(),
        name="add_classroom",
    ),
    path(
        "add/home-work/",
        views.HomeWorkCreateView.as_view(),
        name="add_home_work",
    ),
    # DETAILS
    path(
        "roll/<pk>/detail/",
        views.RollDetailView.as_view(),
        name="detail_student",
    ),
    path(
        "course/<pk>/detail/",
        views.CourseDetailView.as_view(),
        name="detail_course",
    ),
    path(
        "subject/<pk>/detail/",
        views.SubjectDetailView.as_view(),
        name="detail_subject",
    ),
    path(
        "class/<pk>/detail/",
        views.ClassroomDetailView.as_view(),
        name="detail_classroom",
    ),
    path(
        "teacher/<pk>/detail/",
        views.TeacherDetailView.as_view(),
        name="detail_teacher",
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
