from django.contrib.auth.models import Group


def format_grades(course, subject=None, student=None):
    a = None
    b = None
    c = None
    __student = None
    grades = []

    if subject:
        subjects = course.subjects.filter(pk=subject)
    else:
        subjects = course.subjects.all()

    if student:
        rolls = course.rolls.filter(student=student)
    else:
        rolls = course.rolls.all()

    for roll in rolls:
        for __subject in subjects:
            for grade in __subject.grades.filter(student=roll.student):
                __student = grade.student
                if grade.section.name == "A":
                    a = grade or None
                elif grade.section.name == "B":
                    b = grade or None
                elif grade.section.name == "C":
                    c = grade or None
            if __student is not None:
                grades.append(
                    {
                        "student": __student,
                        "subject": __subject,
                        "a": a,
                        "b": b,
                        "c": c,
                    }
                )

            a = None
            b = None
            c = None
            __student = None
    return grades


def add_user_to_group(user=None):
    if user:
        group, _ = Group.objects.get_or_create(name=user.role)
        user.groups.add(group)
