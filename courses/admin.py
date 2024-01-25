from django.contrib import admin
from .models import  Course, Module,Content,File,Task
from django.contrib import admin
from .models import Category,CourseName,Reference,File,CourseAccess



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category', 'slug']
    prepopulated_fields = {'slug': ('category',)}


# @admin.register(SubCategory)
# class SubCategory(admin.ModelAdmin):
#     list_display = "name",

    
    


@admin.register(CourseName)
class CourseNameAdmin(admin.ModelAdmin):
    list_display = ['name']
    


class ModuleInline(admin.StackedInline):
    model = Module


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    actions = ["publish_selected","unpublish_selected"]
    list_display = ['created','has_practice','published','ceu']
    list_filter = ['created',]
    search_fields = [ 'overview']
    prepopulated_fields = {'slug': ('overview',)}
    inlines = [ModuleInline]

    #publish course
    def publish_selected(self, request, queryset):
        queryset.update(published=True)

    #unpublish course
    def unpublish_selected(self, request, queryset):
        queryset.update(published=False)




admin.site.register(File)
admin.site.register(Task)
admin.site.register(Reference)
admin.site.register(CourseAccess)



