from django.contrib import messages
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    FormView,
    ListView,
    UpdateView,
)

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

from . import utils
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
            "grades": utils.format_grades(
                course=self.object.course,
                student=self.object.student,
                subject=subject,
            ),
        }
        context["form"] = GetGradeForm(self.request.user)
        return context


# Only staff
class RollCreateView(FormView):
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
        utils.add_user_to_group(student)

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


class RollUpdateView(UpdateView):
    template_name = "sms/forms.html"
    form_class = StudentRegistrationForm
    model = Roll
    success_url = reverse_lazy("sms:dashboard")

    def get_initial(self):
        profile = self.get_object().student.profile
        initial_data = super().get_initial()

        initial_data["first_name"] = profile.first_name
        initial_data["last_name"] = profile.last_name
        initial_data["date_of_birth"] = profile.dob
        initial_data["phone_no"] = profile.phone_no
        initial_data["parent_phone_no"] = profile.parent_phone_no
        initial_data["parent_address"] = profile.parent_address
        initial_data["parent_name"] = profile.parent_name
        initial_data["address"] = profile.address
        return initial_data

    def form_valid(self, form):
        data = form.cleaned_data

        roll = form.save()

        profile = Profile.objects.get(user=roll.student)
        for key, value in data.items():
            setattr(profile, key, value)
        profile.save()

        return super().form_valid(form)


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

        if not query:
            messages.info(self.request, "No record found!")
            query = self.object_list

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
class TeacherCreateView(FormView):
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
        teacher = t_form.save()
        utils.add_user_to_group(teacher)

        profile = Profile(user=teacher)
        for key, value in form.cleaned_data.items():
            setattr(profile, key, value)
        profile.save()

        contract = form.save(commit=False)
        contract.teacher = teacher
        contract.save()

        return super().form_valid(form)


class TeacherUpdateView(UpdateView):
    template_name = "sms/forms.html"
    model = TeacherContract
    form_class = TeacherRegistrationForm
    success_url = reverse_lazy("sms:list_teacher")

    def get_initial(self):
        initial_data = super().get_initial()
        contract = self.get_object()
        teacher = contract.teacher
        initial_data["first_name"] = teacher.profile.first_name
        initial_data["last_name"] = teacher.profile.last_name
        initial_data["date_of_birth"] = teacher.profile.dob
        initial_data["phone_no"] = teacher.profile.phone_no
        initial_data["address"] = teacher.profile.address
        initial_data["category"] = contract.category
        initial_data["classroom"] = contract.classroom.all()
        initial_data["subject"] = contract.subject.all()
        initial_data["status"] = contract.status
        initial_data["date_start"] = contract.date_start

        return initial_data

    def form_valid(self, form):
        data = form.cleaned_data
        contract = self.get_object()
        profile = Profile.objects.get(user=contract.teacher)

        for key, value in data.items():
            setattr(profile, key, value)
        profile.save()
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

        # Filter by classroom and subject
        context["form"] = GetGradeForm(user=self.request.user)
        classroom = self.request.GET.get("classroom")
        subject = self.request.GET.get("subject")

        if classroom and subject:
            course = Classroom.objects.get(pk=classroom).course
            queryset = utils.format_grades(course=course, subject=subject)
        elif classroom and not subject:
            course = Classroom.objects.get(pk=classroom).course
            queryset = utils.format_grades(course=course)
        elif not classroom and subject:
            course = Course.objects.first()
            if not course:
                context["grades"] = []
                return context
            queryset = utils.format_grades(course=course, subject=subject)
        else:
            course = Course.objects.first()
            if not course:
                context["grades"] = []
                return context
            queryset = utils.format_grades(course=course)

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
        context["grade"] = utils.format_grades(course, student=student)
        return context


# Only Teacher
class GradeCreateView(CreateView):
    template_name = "sms/forms.html"
    model = Grade
    form_class = GradeForm
    success_url = reverse_lazy("sms:add_grade")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = GradeForm(user=self.request.user)
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
