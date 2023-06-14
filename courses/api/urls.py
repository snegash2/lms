from django.urls import path
from . import views
app_name = 'courses'
urlpatterns = [
        path('category/',views.CategoryListView.as_view(),name='category_list'),
        path('category/<pk>/',views.CategoryDetailView.as_view(),name='category_detail'),
        path('courses/<pk>/enroll/',views.CourseEnrollView.as_view(),name='course_enroll'),
        
]