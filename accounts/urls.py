from django.urls import  path,include
from .views import register,edit


app_name = "accounts"
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', register, name='register'),
    path('edit/', edit, name='edit'),
]