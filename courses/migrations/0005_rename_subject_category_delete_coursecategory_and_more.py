# Generated by Django 4.1 on 2023-06-01 15:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_coursecategory_slug'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Subject',
            new_name='Category',
        ),
        migrations.DeleteModel(
            name='CourseCategory',
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['title'], 'verbose_name': 'Category'},
        ),
        migrations.AddField(
            model_name='course',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='courses.category', verbose_name='Course Name'),
        ),
    ]
