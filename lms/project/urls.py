from django.conf import  settings
from django.conf.urls.static import static
from courses.views import CourseListView
from django.contrib import admin
from django.urls import path, include
from lms.project.views import index
from django.contrib.auth import views as auth_views
from filebrowser.sites import site

urlpatterns = [
    path('admin/filebrowser/', site.urls),
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(),name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(),name='logout'),
    path('course/', include('courses.urls')),
    path('students/', include('students.urls')),
    # path('', index, name='index'),
    path('', CourseListView.as_view(), name='course_list'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)