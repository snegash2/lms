from django.urls import path
from .views import landing_page
from django.urls import path
from .views import filter_courses



urlpatterns = [
    path('',landing_page,name = "landing"),
    path('filter-courses/', filter_courses, name='filter_courses')
]