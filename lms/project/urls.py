from django.conf import  settings

from django.contrib import admin
from django.urls import path

from lms.project.views import index

print(settings.DEBUG)
print(settings.SECRET_KEY)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index')
]

