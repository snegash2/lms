from django.contrib import admin
from .models import  Course, Module
from django.contrib import admin
from .models import File
from .models import Category,CourseName





# custom actions






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
    actions = ["publish_all","unpublish_all"]
    list_display = ['created','has_practice','published','ceu']
    list_filter = ['created',]
    search_fields = [ 'overview']
    prepopulated_fields = {'slug': ('overview',)}
    inlines = [ModuleInline]

    #publish course
    def publish_all(self, request, queryset):
        queryset.update(published=True)


    #unpublish course
    def unpublish_all(self, request, queryset):
        queryset.update(published=False)




