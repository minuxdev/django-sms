from django.views.generic import DetailView, ListView

from users.models import Student, Teacher

from .models import Classroom, Course, HomeWork, Roll


# ROLLS
class RollView(ListView):
    template_name = "sms/list.html"
    model = Roll
    context_object_name = "students"


class RollDetailView(DetailView):
    template_name = "sms/details.html"
    model = Roll
    context_object_name = "student"


# TEACHER
class TeacherView(ListView):
    template_name = "sms/list.html"
    model = Teacher
    context_object_name = "teachers"


class TeacherDetailView(DetailView):
    template_name = "sms/details.html"
    model = Teacher
    context_object_name = "teacher"


# CLASSROOM
class ClassroomView(ListView):
    template_name = "sms/list.html"
    model = Classroom
    context_object_name = "classrooms"


class ClassroomDetailView(DetailView):
    template_name = "sms/details.html"
    model = Classroom
    context_object_name = "classroom"


# COURSE
class CourseView(ListView):
    template_name = "sms/list.html"
    model = Course
    context_object_name = "courses"


class CourseDetailView(DetailView):
    template_name = "sms/details.html"
    model = Course
    context_object_name = "course"


# GRADE
def format_student_grades(student):
    a = {}
    b = {}
    c = {}
    marks = student.grades.all()
    for mark in marks:
        if mark.section == "A":
            a = mark or None
        elif mark.section == "B":
            b = mark or None
        elif mark.section == "C":
            c = mark or None

    return {
        "student": student,
        "a": a,
        "b": b,
        "c": c,
    }


class GradeView(ListView):
    template_name = "sms/list.html"
    model = Student

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["grades"] = []
        students = Student.objects.all()
        for student in students:
            context["grades"].append(format_student_grades(student))
        return context


class GradeDetailView(DetailView):
    template_name = "sms/details.html"
    model = Student
    context_object_name = "grade"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        student = self.object
        context["grade"] = format_student_grades(student)
        return context


class HomeWrokView(ListView):
    template_name = "sms/list.html"
    model = HomeWork
    context_object_name = "homeworks"


class HomeWrokDetailView(DetailView):
    template_name = "sms/details.html"
    model = HomeWork
    context_object_name = "homework"
