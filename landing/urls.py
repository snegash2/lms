from django.urls import path
from .views import landing_page
from django.urls import path
from .views import filter_courses,get_course_name,user_global_settings_update,verify_egiliable_student_ajax,student_enrolloment
from courses.views import delete_module,AssCreateView




urlpatterns = [
    path('',landing_page,name = "landing"),
    path('filter-courses/', filter_courses, name='filter_courses'),
    path('get_course_name/',get_course_name, name='get_course_name'),
    path('eligibility_ajax/',verify_egiliable_student_ajax,name='egiliablity_ajax'),
    path('student_enrolloment/',student_enrolloment,name='student_enrolloment'),
    path('user_global_settings_update/',user_global_settings_update,name="user_global_settings_update"),
    path('ass_create/',AssCreateView.as_view(),name='ass_create'),
    path('module_delete/',delete_module,name = "delete_module")
]

