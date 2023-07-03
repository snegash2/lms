# Generated by Django 4.1 on 2023-06-30 19:29

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200, unique=True)),
            ],
            options={
                'verbose_name': 'Category',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='CourseName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Course Name ')),
                ('category', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='courses.category', verbose_name='Category')),
            ],
        ),
        migrations.RemoveField(
            model_name='course',
            name='subject',
        ),
        migrations.RemoveField(
            model_name='course',
            name='title',
        ),
        migrations.AddField(
            model_name='course',
            name='ceu',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='course',
            name='has_practice',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='course',
            name='published',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='course',
            name='reason_not_published',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
        migrations.AlterField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='courses_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='module',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True),
        ),
        migrations.DeleteModel(
            name='Subject',
        ),
        migrations.AddField(
            model_name='course',
            name='course_name',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='names', to='courses.coursename', verbose_name='Name'),
        ),
    ]