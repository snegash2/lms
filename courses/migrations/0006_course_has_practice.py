# Generated by Django 4.1 on 2023-05-29 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_coursecategory_delete_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='has_practice',
            field=models.BooleanField(default=False),
        ),
    ]
