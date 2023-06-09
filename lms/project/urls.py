from django.conf import  settings
from django.conf.urls.static import static
from courses.views import CourseListView
from django.contrib import admin
from django.urls import path,re_path, include
from lms.project.views import index






urlpatterns = [
  
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('quiz/',include('exam.quiz.urls')),   
    path('course/', include('courses.urls')),
    path('students/', include('students.urls')),
    path('api/', include('courses.api.urls', namespace='api')),
    path('', CourseListView.as_view(), name='course_list'),
    path('chat/', include('chat.urls', namespace='chat')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    # path('social-auth/',include('social_django.urls', namespace='social')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)