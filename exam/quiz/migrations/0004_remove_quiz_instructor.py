# Generated by Django 4.1 on 2024-02-11 13:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_quiz_instructor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='instructor',
        ),
    ]
