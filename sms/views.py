from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from sms.forms import (
    ClassroomForm,
    CourseForm,
    GetClassForm,
    GradeForm,
    HomeWorkForm,
    RollForm,
    SubjectForm,
)
from users.models import CustomUser, Student, Teacher

from .models import Classroom, Course, Grade, HomeWork, Roll, Subject


# ROLLS
class RollView(ListView):
    template_name = "sms/list.html"
    model = Roll
    context_object_name = "students"


class RollDetailView(DetailView):
    template_name = "sms/details.html"
    model = Roll
    context_object_name = "student"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.object.student)
        # context["student"] = list(format_student_grades(self.object.student))
        return context


class RollCreateView(CreateView):
    template_name = "sms/forms.html"
    form_class = RollForm
    model = Roll
    success_url = reverse_lazy("sms:dashboard")


# TEACHER
class TeacherView(ListView):
    template_name = "sms/list.html"
    model = Teacher
    context_object_name = "teachers"


class TeacherDetailView(DetailView):
    template_name = "sms/details.html"
    model = Teacher
    context_object_name = "teacher"


# COURSE
class CourseView(ListView):
    template_name = "sms/list.html"
    model = Course
    context_object_name = "courses"


class CourseDetailView(DetailView):
    template_name = "sms/details.html"
    model = Course
    context_object_name = "course"


class CourseCreateView(CreateView):
    template_name = "sms/forms.html"
    model = Course
    form_class = CourseForm
    success_url = reverse_lazy("sms:add_course")


# SUBJECT
class SubjectView(ListView):
    model = Subject
    template_name = "sms/list.html"
    context_object_name = "subjects"


class SubjectDetailView(DetailView):
    model = Subject
    template_name = "sms/details.html"
    context_object_name = "subject"


class SubjectCreateView(CreateView):
    model = Subject
    template_name = "sms/forms.html"
    form_class = SubjectForm
    success_url = reverse_lazy("sms:add_subject")


# CLASSROOM
class ClassroomView(ListView):
    template_name = "sms/list.html"
    model = Classroom
    context_object_name = "classrooms"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Filter classes based on query
        course = self.request.GET.get("course", None)
        if course is not None and course != "":
            context["classrooms"] = Classroom.objects.filter(
                course__name=course
            )

        # List filtered classes by user in form
        context["form"] = GetClassForm
        user = self.request.user
        if not user.is_authenticated:
            return context
        if user.is_authenticated:
            if user.role == "STUDENT":
                print(user, user.role)
                # context["form"] = GetClassForm(classroom=user.roll.classroom)
            elif user.role == "TEACHER":
                print(user, user.role)
                # context["form"] = GetClassForm(classroom=user.roll.classroom)
        return context


class ClassroomDetailView(DetailView):
    template_name = "sms/details.html"
    model = Classroom
    context_object_name = "classroom"


class ClassroomCreateView(CreateView):
    template_name = "sms/forms.html"
    model = Classroom
    form_class = ClassroomForm
    success_url = reverse_lazy("sms:add_classroom")


# GRADE
def format_student_grades(course):
    a = None
    b = None
    c = None
    __student = None
    grades = []
    for roll in course.rolls.all():
        for subject in course.subjects.all():
            for grade in subject.grades.filter(student=roll.student):
                __student = grade.student
                print(__student)
                if grade.section == "A":
                    a = grade or None
                elif grade.section == "B":
                    b = grade or None
                elif grade.section == "C":
                    c = grade or None
            if __student is not None:
                grades.append(
                    {
                        "student": __student,
                        "subject": subject,
                        "a": a,
                        "b": b,
                        "c": c,
                    }
                )

            a = None
            b = None
            c = None
            __student = None
    return grades


class GradeView(ListView):
    template_name = "sms/list.html"
    model = Student

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["grades"] = []
        course = Course.objects.first()
        context["grades"] = format_student_grades(course)
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


class GradeCreateView(CreateView):
    template_name = "sms/forms.html"
    model = Grade
    form_class = GradeForm
    success_url = reverse_lazy("sms:add_grade")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = GradeForm(teacher=self.request.user)
        return context


class HomeWrokView(ListView):
    template_name = "sms/list.html"
    model = HomeWork
    context_object_name = "homeworks"


class HomeWrokDetailView(DetailView):
    template_name = "sms/details.html"
    model = HomeWork
    context_object_name = "homework"


class HomeWorkCreateView(CreateView):
    template_name = "sms/forms.html"
    model = HomeWork
    form_class = HomeWorkForm
    success_url = reverse_lazy("sms:add_home_work")
