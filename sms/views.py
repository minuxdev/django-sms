from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from sms.forms import (
    ClassroomForm,
    CourseForm,
    GetClassForm,
    GetCourseForm,
    GetGradeForm,
    GetStudentForm,
    GetSubjectForm,
    GetTeacherForm,
    GradeForm,
    HomeWorkForm,
    SectionForm,
    StudentRegistrationForm,
    SubjectForm,
    TeacherRegistrationForm,
)
from users.forms import StudentForm, TeacherForm, UserRegistrationForm
from users.models import Profile, Student, Teacher

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
from .utils import format_grades


# ROLLS
# Permissions (only teachers and staff)
class RollView(ListView):
    template_name = "sms/list.html"
    model = Roll
    context_object_name = "students"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Filter by classroom
        context["form"] = GetStudentForm()
        classroom = self.request.GET.get("classroom")
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


# Only staff
class RollCreateView(CreateView):
    template_name = "sms/forms.html"
    form_class = StudentRegistrationForm
    model = Roll
    success_url = reverse_lazy("sms:dashboard")

    @transaction.atomic
    def form_valid(self, form):
        data = form.cleaned_data
        sid = Student.objects.count() + 1
        s_data = {
            "username": f"1003{sid}",
            "password1": f"1003{sid}@2024",
            "password2": f"1003{sid}@2024",
            "role": "STUDENT",
        }

        # Create student
        s_form = StudentForm(data=s_data)
        student = s_form.save()

        profile = Profile(user=student)
        for key, value in data.items():
            setattr(profile, key, value)
        profile.save()

        role = form.save(commit=False)
        role.student = student
        role.save()

        # Create parent
        if form.data["parent_name"]:
            pid = Parent.objects.count() + 1
            p_data = {
                "username": f"3003{pid}",
                "password1": f"3003{pid}@2024",
                "password2": f"3003{pid}@2024",
                "role": "PARENT",
            }

            p_form = UserRegistrationForm(data=p_data)
            parent = p_form.save()
            _parent = Parent.objects.create(
                user=parent,
                full_name=data["parent_name"],
                address=data["address"],
                phone_no=data["parent_phone_no"],
            )
            _parent.student.add(student)

        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


# TEACHER
# Only staff
class TeacherView(ListView):
    template_name = "sms/list.html"
    model = TeacherContract
    context_object_name = "teachers"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = GetTeacherForm(self.request.user or None)
        class_id = self.request.GET.get("classroom")
        subject_id = self.request.GET.get("subject")
        status = self.request.GET.get("status")
        query = None

        if not status:
            return context

        if class_id == "" and subject_id == "":
            query = TeacherContract.objects.filter(
                status=status,
            )
        elif class_id == "" and subject_id != "":
            query = TeacherContract.objects.filter(
                subject__id=subject_id,
                status=status,
            )
        elif class_id != "" and subject_id == "":
            query = TeacherContract.objects.filter(
                classroom__id=class_id,
                status=status,
            )

        else:
            query = TeacherContract.objects.filter(
                classroom__id=class_id,
                subject__id=subject_id,
                status=status,
            )

        context["teachers"] = query
        return context


class TeacherDetailView(DetailView):
    template_name = "sms/details.html"
    model = TeacherContract
    context_object_name = "teacher"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# Only Staff
class TeacherCreateView(CreateView):
    template_name = "sms/forms.html"
    model = TeacherContract
    form_class = TeacherRegistrationForm
    success_url = reverse_lazy("sms:list_teacher")

    @transaction.atomic
    def form_valid(self, form):
        __id = Teacher.objects.count() + 1
        data = {
            "username": f"2003{__id}",
            "password1": f"2003{__id}@2024",
            "password2": f"2003{__id}@2024",
            "role": "TEACHER",
        }
        t_form = TeacherForm(data=data)
        t = Teacher.objects.all()
        for i in t:
            print(i.username)
        print(t_form.data)
        teacher = t_form.save()

        profile = Profile(user=teacher)
        for key, value in form.cleaned_data.items():
            setattr(profile, key, value)
        profile.save()

        contract = form.save(commit=False)
        contract.teacher = teacher
        contract.save()

        return super().form_valid(form)


# COURSE
class CourseView(ListView):
    template_name = "sms/list.html"
    model = Course
    context_object_name = "courses"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Filter by course name
        context["form"] = GetCourseForm
        course = self.request.GET.get("course")
        if course:
            context["courses"] = Course.objects.filter(name=course)

        return context


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Filter by course
        context["form"] = GetSubjectForm
        cid = self.request.GET.get("course")
        if cid:
            context["subjects"] = Subject.objects.filter(course=cid)

        return context


class SubjectDetailView(DetailView):
    model = Subject
    template_name = "sms/details.html"
    context_object_name = "subject"


class SubjectCreateView(CreateView):
    model = Subject
    template_name = "sms/forms.html"
    form_class = SubjectForm
    success_url = reverse_lazy("sms:add_subject")

    @transaction.atomic
    def form_valid(self, form):
        subject = form.save()
        subject.section.set(form.cleaned_data["section"])

        return super().form_valid(form)


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

        # Filter classroom by user in form
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
        queryset = self.object_list
        print(queryset)

        # Filter by classroom and subject
        context["form"] = GetGradeForm(user=self.request.user)
        classroom = self.request.GET.get("classroom")
        subject = self.request.GET.get("subject")

        if classroom and subject:
            course = Classroom.objects.get(pk=classroom).course
            queryset = format_grades(course=course, subject=subject)
        elif classroom and not subject:
            course = Classroom.objects.get(pk=classroom).course
            queryset = format_grades(course=course)
        elif not classroom and subject:
            course = Course.objects.first()
            if not course:
                context["grades"] = []
                return context
            queryset = format_grades(course=course, subject=subject)

        context["grades"] = queryset
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


# Only Teacher
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


# Only Teacher
class HomeWorkCreateView(CreateView):
    template_name = "sms/forms.html"
    model = HomeWork
    form_class = HomeWorkForm
    success_url = reverse_lazy("sms:add_home_work")


class SectionView(ListView):
    template_name = "sms/list.html"
    model = Section
    context_object_name = "sections"


class SectionDetailView(DetailView):
    template_name = "sms/details.html"
    model = Section
    context_object_name = "section"


class SectionCreateView(CreateView):
    template_name = "sms/forms.html"
    model = Section
    form_class = SectionForm
    success_url = reverse_lazy("sms:list_section")
