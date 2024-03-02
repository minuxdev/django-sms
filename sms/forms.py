from django import forms

from sms.models import (
    Classroom,
    Course,
    Grade,
    HomeWork,
    Roll,
    Section,
    Subject,
    TeacherContract,
)


class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=40)
    last_name = forms.CharField(max_length=40)
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"})
    )
    phone_no = forms.CharField(widget=forms.NumberInput)
    address = forms.CharField(max_length=255, required=False)


class StudentRegistrationForm(RegistrationForm):
    parent_name = forms.CharField(max_length=100, required=False)
    parent_phone_no = forms.CharField(widget=forms.NumberInput)

    class Meta:
        model = Roll
        exclude = (
            "student",
            "id",
        )


class TeacherRegistrationForm(RegistrationForm):
    class Meta:
        model = TeacherContract
        exclude = ("id", "date_celebrate", "date_end", "teacher")
        widgets = {
            "date_start": forms.DateInput(attrs={"type": "date"}),
            "subject": forms.SelectMultiple,
            "classroom": forms.SelectMultiple,
        }

    field_order = (
        "first_name",
        "last_name",
        "date_of_birth",
        "phone_no",
        "address",
        "category",
        "classroom",
        "subject",
        "status",
        "date_start",
    )


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = ("id",)
        widgets = {
            "year": forms.DateInput(attrs={"type": "date"}),
        }


class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        exclude = ("id",)
        widgets = {
            "year": forms.DateInput(attrs={"type": "date"}),
        }


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ("name", "description")


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        exclude = ("id",)
        widgets = {
            "year": forms.DateInput(attrs={"type": "date"}),
            "section": forms.CheckboxSelectMultiple,
        }


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        exclude = (
            "year",
            "id",
            "classroom",
            "section_average",
            "test_average",
            "teacher",
        )
        widgets = {
            "subject": forms.RadioSelect,
            "section": forms.RadioSelect,
        }

    def __init__(self, teacher=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if teacher:
            queryset = Subject.objects.filter(teacher=teacher)
            self.fields["subject"].queryset = queryset
            self.fields["subject"].initial = queryset[0] if queryset else None


class HomeWorkForm(forms.ModelForm):
    class Meta:
        model = HomeWork
        exclude = ("date_create", "id")


# Form Filters
class GetClassForm(forms.Form):
    queryset = Course.objects.all()
    course = forms.ModelChoiceField(queryset=queryset, widget=forms.Select)

    def __init__(self, user=None, **kwargs):
        super().__init__(**kwargs)

        if user and user.role == "TEACHER":
            self.fields[
                "course"
            ].queryset = user.teachercontract.classroom.all()


class GetGradeForm(forms.Form):
    c_queryset = Classroom.objects.all()
    s_queryset = Subject.objects.all()
    classroom = forms.ModelChoiceField(
        queryset=c_queryset,
        widget=forms.Select,
        required=False,
    )
    subject = forms.ModelChoiceField(
        queryset=s_queryset,
        widget=forms.Select,
        required=False,
    )

    def __init__(self, user=None, **kwargs):
        super().__init__(**kwargs)
        if user:
            if user.role == "STUDENT":
                self.fields["classroom"].widget = forms.HiddenInput()
                self.fields[
                    "subject"
                ].queryset = user.roll.course.subjects.all()


class GetStudentForm(forms.Form):
    queryset = Classroom.objects.all()
    classroom = forms.ModelChoiceField(
        queryset=queryset,
    )


class GetCourseForm(forms.Form):
    queryset = Course.objects.all()
    course = forms.ModelChoiceField(
        queryset=queryset,
    )


class GetTeacherForm(forms.Form):
    subjects = Subject.objects.all()
    classrooms = Classroom.objects.all()
    choice = TeacherContract.STATUS.choices
    subject = forms.ModelChoiceField(queryset=subjects, required=False)
    classroom = forms.ModelChoiceField(queryset=classrooms, required=False)
    status = forms.ChoiceField(
        choices=choice, initial=choice[1], required=False
    )

    def __init__(self, user=None, **kwargs):
        super().__init__(**kwargs)
        if user and user.role == "STUDENT":
            self.fields["classroom"].queryset = user.roll.classroom.all()
            self.fields["subject"].queryset = user.roll.course.subjects.all()
            self.fields["status"].widget = forms.HiddenInput()


class GetSubjectForm(forms.Form):
    courses = Course.objects.all()
    sections = Section.objects.all()
    course = forms.ModelChoiceField(
        queryset=courses,
    )
