from django.urls import path
from . import views
from django.views.decorators.cache import cache_page

# app_name = "students"
urlpatterns = [
    path('register/',views.StudentRegistrationView.as_view(),name='student_registration'),
    path('dashboard/<pk>/',views.StudentDashboard.as_view(),name='student-dashboard'),
    path('enroll-course/',views.StudentEnrollCourseView.as_view(),name='student_enroll_course'),
    path('update-profile/<int:pk>/',views.StudentProfileView.as_view(),name='student_update_profile'),
    path('courses/',views.StudentCourseListView.as_view(),name='student_course_list'),
    path('course/<pk>/',cache_page(60 * 15)(views.StudentCourseDetailView.as_view()),name='student_course_detail'),
    path('course/<pk>/<module_id>/',cache_page(60 * 15)(views.StudentCourseDetailView.as_view()),name='student_course_detail_module'),
]