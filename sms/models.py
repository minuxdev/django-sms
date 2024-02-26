from django.db import models

from users.models import Student, Teacher


class SECTION(models.TextChoices):
    A = "A", "A"
    B = "B", "B"
    C = "C", "C"


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
    name = models.CharField(max_length=100)
    year = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.year}"


class Subject(models.Model):
    course = models.ManyToManyField(
        to=Course,
        blank=True,
        related_name="subjects",
    )
    teacher = models.ManyToManyField(
        to=Teacher, blank=True, related_name="subjects"
    )
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
    section = models.CharField(
        max_length=50, choices=SECTION.choices, default=SECTION.A
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
    classroom = models.ManyToManyField(to=Classroom, blank=True)
    topic = models.CharField(max_length=255)
    content = models.TextField(null=True, blank=True)
    date_create = models.DateTimeField(auto_now_add=True)
    date_close = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.topic)
