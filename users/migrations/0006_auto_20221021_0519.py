# Generated by Django 3.2.5 on 2022-10-21 05:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_is_student_user_is_teacher'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_student',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_teacher',
        ),
    ]
