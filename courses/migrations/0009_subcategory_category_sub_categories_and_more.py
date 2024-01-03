# Generated by Django 4.1 on 2024-01-02 20:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_alter_course_course_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250, null=True, verbose_name='Sub-Category')),
            ],
            options={
                'verbose_name': 'Sub-Category',
                'verbose_name_plural': 'Sub-Categories',
            },
        ),
        migrations.AddField(
            model_name='category',
            name='sub_categories',
            field=models.ManyToManyField(to='courses.subcategory'),
        ),
        migrations.AlterField(
            model_name='course',
            name='sub_category',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='courses.subcategory', verbose_name='Sub Category'),
        ),
        migrations.DeleteModel(
            name='CourseCategory',
        ),
    ]
