# Generated by Django 5.0.1 on 2024-01-16 06:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crendential', '0002_crendential_course'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='crendential',
            name='name',
        ),
    ]
