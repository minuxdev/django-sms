from django.db import models
from django.utils import timezone

from users.models import CustomUser, Student, Teacher


class Section(models.Model):
    name = models.CharField(max_length=20, default="A", unique=True)
    description = models.TextField(max_length=300, null=True, blank=True)

    def __str__(self):
        return str(self.name)


class Course(models.Model):
    name = models.CharField(max_length=100)
    year = models.DateField(auto_now=True)

    def __str__(self):
        year = self.year.year
        return f"{self.name} - {year}"


class Classroom(models.Model):
    course = models.ForeignKey(
        to=Course,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="classrooms",
    )
    teacher = models.ManyToManyField(
        to=Teacher,
        blank=True,
        related_name="classrooms",
    )
    name = models.CharField(max_length=100)
    year = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.year}"


class Subject(models.Model):
    class STATUS(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        CANCELED = "CANCELED", "Canceled"

    course = models.ManyToManyField(
        to=Course,
        blank=True,
        related_name="subjects",
    )
    teacher = models.ManyToManyField(
        to=Teacher, blank=True, related_name="subjects"
    )
    name = models.CharField(max_length=100)
    section = models.ManyToManyField(
        to=Section,
        blank=True,
        related_name="subjects",
    )
    year = models.DateField(auto_now=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS.choices,
        default=STATUS.ACTIVE,
    )

    def __str__(self):
        return str(self.name)


class Roll(models.Model):
    course = models.ForeignKey(
        to=Course,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="rolls",
    )
    classroom = models.ForeignKey(
        to=Classroom,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="rolls",
    )
    student = models.OneToOneField(
        to=Student, on_delete=models.CASCADE, null=True, blank=True
    )
    year = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.student)


class Grade(models.Model):
    section = models.ForeignKey(
        to=Section,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="grades",
    )
    subject = models.ForeignKey(
        to=Subject,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="grades",
    )
    classroom = models.ForeignKey(
        to=Classroom,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="grades",
    )
    student = models.ForeignKey(
        to=Student,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="grades",
    )
    teacher = models.ForeignKey(
        to=Teacher,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="t_grades",
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


class HomeWork(models.Model):
    teacher = models.ForeignKey(
        to=Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="homeworks",
    )
    classroom = models.ManyToManyField(
        to=Classroom,
        blank=True,
        related_name="homeworks",
    )
    subject = models.ForeignKey(
        to=Subject,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="homeworks",
    )
    topic = models.CharField(max_length=255)
    content = models.TextField(null=True, blank=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_close = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.topic)


class TeacherContract(models.Model):
    class STATUS(models.TextChoices):
        PENDING = "PENDING", "Pending"
        ACTIVE = "ACTIVE", "Active"
        CANCELED = "CANCELED", "Canceled"
        SUSPENDED = "SUSPENDED", "Suspended"
        END = "ENDED", "Ended"

    teacher = models.OneToOneField(
        to=Teacher, on_delete=models.SET_NULL, null=True, blank=True
    )
    classroom = models.ManyToManyField(
        to=Classroom,
        blank=True,
        related_name="classrooms",
    )
    subject = models.ManyToManyField(
        to=Subject, blank=True, related_name="subjects"
    )
    category = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(
        max_length=10, choices=STATUS.choices, default=STATUS.PENDING
    )
    date_celebrate = models.DateField(auto_now_add=True)
    date_start = models.DateField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.teacher)

    def save(self, **kwargs):
        if self.status == "ENDED":
            self.date_end = timezone.now()
        else:
            self.date_end = None
        return super().save(**kwargs)


class Parent(models.Model):
    user = models.OneToOneField(to=CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    student = models.ManyToManyField(
        to=Student, blank=True, related_name="parents"
    )
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_no = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return str(self.full_name)
