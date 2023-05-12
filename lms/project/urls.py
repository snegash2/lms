from django.conf import  settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include
from lms.project.views import index
from django.contrib.auth import views as auth_views

print(settings.DEBUG)
print(settings.SECRET_KEY)
urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(),name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(),name='logout'),
    path('admin/', admin.site.urls),
    path('course/', include('courses.urls')),
    path('', index, name='index')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)