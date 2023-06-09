from django.contrib import admin
from .models import  Course, Module
from django.contrib import admin
from .models import File
from .models import Category,CourseName



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}
    


@admin.register(CourseName)
class CourseNameAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    


class ModuleInline(admin.StackedInline):
    model = Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['created','has_practice','published','ceu']
    list_filter = ['created',]
    search_fields = [ 'overview']
    prepopulated_fields = {'slug': ('overview',)}
    inlines = [ModuleInline]



