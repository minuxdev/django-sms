from django import forms

from sms.models import Classroom, Course, Grade, HomeWork, Roll, Subject


class RollForm(forms.ModelForm):
    first_name = forms.CharField(max_length=40)
    last_name = forms.CharField(max_length=40)
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"})
    )
    phone_no = forms.CharField(widget=forms.NumberInput)
    guardian_name = forms.CharField(max_length=100, required=False)
    guardian_phone_no = forms.CharField(widget=forms.NumberInput)
    address = forms.CharField(max_length=255, required=False)

    class Meta:
        model = Roll
        exclude = (
            "student",
            "id",
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


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        exclude = ("id",)
        widgets = {
            "year": forms.DateInput(attrs={"type": "date"}),
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

    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop("teacher", None)
        super().__init__(*args, **kwargs)
        if teacher:
            self.fields["subject"].queryset = Subject.objects.filter(
                teacher=teacher
            )


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
        if user.role == "TEACHER":
            pass


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
                # self.fields["classroom"].widgets = forms.HiddenInput()
                del self.fields["classroom"]  # Hide this field instead
                self.fields[
                    "subject"
                ].queryset = user.roll.course.subjects.all()


class GetStudentForm(forms.Form):
    queryset = Classroom.objects.all()
    classroom = forms.ModelChoiceField(queryset=queryset, initial=queryset[0])
