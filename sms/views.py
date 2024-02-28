from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from sms.forms import (
    ClassroomForm,
    CourseForm,
    GetClassForm,
    GetGradeForm,
    GetStudentForm,
    GradeForm,
    HomeWorkForm,
    RollForm,
    SubjectForm,
)
from users.forms import StudentForm
from users.models import CustomUser, Profile, Student, Teacher

from .models import Classroom, Course, Grade, HomeWork, Roll, Subject
from .utils import format_grades


# ROLLS
class RollView(ListView):
    template_name = "sms/list.html"
    model = Roll
    context_object_name = "students"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = GetStudentForm
        classroom = self.request.GET.get("classroom", None)

        if classroom:
            context["students"] = Roll.objects.filter(classroom=classroom)
        return context


class RollDetailView(DetailView):
    template_name = "sms/details.html"
    model = Roll
    context_object_name = "student"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        subject = self.request.GET.get("subject", None)
        context["student"] = {
            "roll": self.object,
            "grades": format_grades(
                course=self.object.course,
                student=self.object.student,
                subject=subject,
            ),
        }
        context["form"] = GetGradeForm(self.request.user)
        return context


class RollCreateView(CreateView):
    template_name = "sms/forms.html"
    form_class = RollForm
    model = Roll
    success_url = reverse_lazy("sms:dashboard")

    def form_valid(self, form):
        __id = Student.objects.count() + 1
        data = {
            "username": f"1003{__id}",
            "password1": f"1003{__id}@2024",
            "password2": f"1003{__id}@2024",
            "role": "STUDENT",
        }
        s_form = StudentForm(data=data)
        student = s_form.save()

        profile = Profile(user=student)
        for key, value in form.cleaned_data.items():
            setattr(profile, key, value)
        profile.save()

        role = form.save(commit=False)
        role.student = student
        role.save()

        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


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
            context["classrooms"] = Classroom.objects.filter(course=course)

        # List filtered classes by user in form
        context["form"] = GetClassForm
        user = self.request.user
        if not user.is_authenticated:
            return context
        if user.is_authenticated:
            context["form"] = GetClassForm(user=user)
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
class GradeView(ListView):
    template_name = "sms/list.html"
    model = Student

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        course = Course.objects.last()

        # Get query parameters
        subject = self.request.GET.get("subject", None)
        classroom = self.request.GET.get("classroom", 1)
        if classroom:
            course = Classroom.objects.get(pk=classroom).course
        context["grades"] = format_grades(
            course,
            subject=subject or course.subjects.first().pk,
        )

        context["form"] = GetGradeForm(user=self.request.user)

        return context


class GradeDetailView(DetailView):
    template_name = "sms/details.html"
    model = Student
    context_object_name = "grade"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        student = self.object.student
        course = student.roll.course
        context["grade"] = format_grades(course, student=student)
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
