from django.contrib import admin
from .models import Subject, Course, Module
from django.contrib import admin
from .models import File
from .models import CourseCategory



@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
   



@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}


class ModuleInline(admin.StackedInline):
    model = Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = [ 'subject', 'created','has_practice','ceu']
    list_filter = ['created', 'subject']
    search_fields = [ 'overview']
    prepopulated_fields = {'slug': ('overview',)}
    inlines = [ModuleInline]



