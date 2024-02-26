# Generated by Django 4.2.9 on 2024-02-25 18:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile'),
        ('sms', '0008_alter_grade_classroom_alter_grade_student_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='grade',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='t_grades', to='users.teacher'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='course',
            field=models.ManyToManyField(blank=True, related_name='subjects', to='sms.course'),
        ),
        migrations.AlterField(
            model_name='subject',
            name='teacher',
            field=models.ManyToManyField(blank=True, related_name='subjects', to='users.teacher'),
        ),
    ]
