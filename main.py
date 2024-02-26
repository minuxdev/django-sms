from sms.models import Course

c1 = Course.objects.first()
a = {}
b = {}
c = {}
student = ""

for subject in c1.subjects.all():
    for grade in subject.grades.all():
        student = grade.student
        if grade.section == "A":
            a = grade
        elif grade.section == "B":
            b = grade
        else:
            c = grade
    print(
        {
            "student": student,
            "subject": subject,
            "a": a,
            "b": b,
            "c": c,
        }
    )
    a = None
    b = None
    c = None
    student = ""
