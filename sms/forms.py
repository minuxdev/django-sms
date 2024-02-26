from django import forms

from sms.models import Classroom, Course, Grade, HomeWork, Roll, Subject


class RollForm(forms.ModelForm):
    class Meta:
        model = Roll
        exclude = (
            "id",
            "student",
        )
        widgets = {
            "year": forms.DateInput(attrs={"type": "date"}),
        }


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


class GetClassForm(forms.Form):
    course = forms.CharField(strip=True, required=False)

    def __init__(self, course=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if course:
            self.fields["course"].queryset = Course.objects.all()
