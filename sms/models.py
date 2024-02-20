import math

from django.db import models
from django.db.models import constraints

from users.models import Student, Teacher


class SECTION(models.TextChoices):
    A = "A", "A"
    B = "B", "B"
    C = "C", "C"


class Course(models.Model):
    name = models.CharField(max_length=100)
    year = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.year}"


class Classroom(models.Model):
    course = models.ForeignKey(
        to=Course, on_delete=models.CASCADE, null=True, blank=True
    )
    name = models.CharField(max_length=100)
    year = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.year}"


class Subject(models.Model):
    course = models.ManyToManyField(
        to=Course,
        blank=True,
    )
    teacher = models.ManyToManyField(to=Teacher, blank=True)
    name = models.CharField(max_length=100)
    section = models.CharField(
        max_length=50, choices=SECTION.choices, default=SECTION.A
    )
    year = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.name)


class Roll(models.Model):
    course = models.ForeignKey(
        to=Course,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="roll",
    )
    classroom = models.ForeignKey(
        to=Classroom,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="roll",
    )
    student = models.OneToOneField(
        to=Student, on_delete=models.CASCADE, null=True, blank=True
    )
    year = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.student)


class Grade(models.Model):
    section = models.CharField(
        max_length=50, choices=SECTION.choices, default=SECTION.A
    )
    subject = models.ForeignKey(
        to=Subject,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="grade",
    )
    classroom = models.ForeignKey(
        to=Classroom,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="grade",
    )
    student = models.ForeignKey(
        to=Student,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="grade",
    )
    test_1 = models.FloatField(default=0, null=True, blank=True)
    test_2 = models.FloatField(default=0, null=True, blank=True)
    test_average = models.FloatField(
        default=0, editable=False, null=True, blank=True
    )
    exam = models.FloatField(default=0, null=True, blank=True)
    section_average = models.FloatField(
        default=0, editable=False, null=True, blank=True
    )
    year = models.DateField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "subject", "section", "year"],
                name="unique_student_grade",
            )
        ]

    def save(self, *args, **kwargs):
        test_av = "%.2f" % ((self.test_1 + self.test_2) / 2 * 0.4)
        self.test_average = float(test_av)
        av = "%.2f" % (self.test_average + self.exam * 0.6)
        self.section_average = round(float(av))

        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.student)
