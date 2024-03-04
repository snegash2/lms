from django.shortcuts import render
from courses.models import Course,Category,CourseName
from django.contrib.auth.models import Group,User
from django.shortcuts import get_object_or_404
from students.forms import CourseEnrollForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from students.models import GlobalSetting
from django.contrib import messages
import json
from django.contrib.auth.models import Group,Permission
from django.core import serializers
from courses.models import CourseAccess
from allauth.account.forms import LoginForm
from django.contrib.auth.forms import PasswordResetForm
from allauth.account.views import PasswordResetView
from django.template.loader import render_to_string
from django import forms
from landing.models import LmsUser
from django.contrib import messages
# from rest_framework import views
# from rest_framework.response import Response
# from rest_framework import status
from django.contrib.auth.forms import PasswordResetForm




class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        
        response = super().form_valid(form)
        if response.status_code == 302:  # Redirect on success
            html_content = render_to_string(self.get_template_names(), context=self.get_context_data())
            return JsonResponse({'success': True, 'message': 'Email sent'})# 'html_content': html_content})
        return response  # Handle errors normally

        # Remember to set content_type and send additional data as needed



@require_POST
def enroll_form(request):
    pass
    


@require_POST
def filter_courses(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        category = None
        # Filter the courses based on the category
        
        category = json.loads(request.body)
        request.session['category'] = category

        try:
          
            if category.get('category') == "All":
                courses = Course.objects.filter(published = True)
            else:
                category = Category.objects.get(category=category.get('category'))
                courses = Course.objects.filter(category=category).filter(published = True)

        except Category.DoesNotExist:
            raise ValueError("Category ")
        # Prepare the data to be sent as JSON
        courses_dict = []
        for course in courses:
            data = {
                "id":course.id,
                "name" : course.name.name,
                "slug": course.slug,
                'image_url':course.image.url,
                'detail':course.detail,
                'students':[student.id for student in course.students.all()],
                'user':request.user.id

            }
            courses_dict.append(data)
        _data = {
            'courses': courses_dict
           
        }
     
        return JsonResponse(_data)









@require_POST
def get_course_name(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        category = None
        # Filter the courses based on the category
        
        category = json.loads(request.body)
        request.session['category'] = category

        try:
            category = Category.objects.get(category=category.get('category'))
            subcategories = CourseName.objects.filter(category = category)
         
                

        except Category.DoesNotExist:
            raise ValueError("Category ")
        # Prepare the data to be sent as JSON
        names = []
        for sub in subcategories:
            names.append(sub.name)
   
        _data = {
            'courses': names
           
        }
     
        return JsonResponse(_data)
    
    
    
class CustomLoginForm(LoginForm):
    first_name = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder':'First name','class':"form-control"}))
    last_name = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder':'Last name','class':""}))
    email = forms.EmailField(label= "", required=True,widget=forms.TextInput(attrs={'placeholder':'Email','class':"form-control"}))  # Make email required
    # username = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder':'Username','class':""}))
    password1 = forms.CharField(label="",widget=forms.PasswordInput(attrs={'class':"form-control w-100"}))
    password2 = forms.CharField(label="",widget=forms.PasswordInput(attrs={'class':"form-check-input form-check-label"}))

def landing_page(request):
    courses = Course.objects.filter(published = True)
    group = None
    instructors = None
 
    try:
        group = Group.objects.get(name='instructors')
    except Group.DoesNotExist:
        pass
    
    users = LmsUser.objects.all()
    if group:
        instructors = group.user_set.count()
        
    user_num = users.count()
    student_num = int(user_num) - int(instructors)
    categories = Category.objects.all()

    context = {
        'courses':courses,
        'instructors':instructors,
        'students_num':student_num,
        'categories':categories,
        'enroll_form': CourseEnrollForm,
        'login_form':LoginForm()
    }

    return render(request, 'landing/index.html',context)






def get_subcategories(request):
    """
    This function is used to retrieve a list of subcategories based on a selected category.

    Parameters:
    request (HttpRequest): The HTTP request object.

    Returns:
    JsonResponse: A JSON response containing a list of subcategory names and IDs.

    """
    category_id = request.GET.get('category_name')  # Get the selected category ID from the AJAX request
    category = get_object_or_404(Category, category_name = cate)  # Get the category object

    subcategories = CourseCategory.objects.filter(category=category)  # Query subcategories based on the selected category

    # Create a list of subcategory names and IDs
    subcategories_data = [{'id': subcategory.id, 'name': subcategory.name} for subcategory in subcategories]

    return JsonResponse(subcategories_data, safe=False)





def user_global_settings_update(request):
    
      if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        data = json.loads(request.body)
        setting = GlobalSetting()
        update = GlobalSetting.objects.get(user = request.user)
        if update:
            update.data_stored = data
            update.save()
        else:
            setting.user = request.user
            setting.data_stored = data
            setting.save()
            
        # messages.success(request,"Global setting updated successfully")
         
        return JsonResponse(data)
      
          
          
          
          
@require_POST
def verify_egiliable_student_ajax(request):
   
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        body = json.loads(request.body)
        studentId = int(body.get("studentId"))
        action  = body.get('action')
       
        course = None
        student = None
        allowed = False
        courseId = int(body.get("courseId"))
    
        try:
            course = Course.objects.get(id = courseId)
            
        except Course.DoesNotExist:
            pass

        try:
            student = User.objects.get(id = studentId)

        except User.DoesNotExist:
            pass
        try:
       
            group = CourseAccess.objects.get(course = course)
            
            if action == "remove":
               
                group.students.remove(student)
                allowed = False
                
            else:
                
                group.students.add(student)
                allowed = True
                
            group.save()
          
        except Course.DoesNotExist:
            print("group ",group.students.all())
            
            
     
            
        json_course = {
            'allowed':True if allowed else False
        }        
        return JsonResponse(json_course)
    
    
    
    
@require_POST
def student_enrolloment(request):
   
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        body = json.loads(request.body)
        studentId = int(body.get("studentId"))
        action  = body.get('action')
       
        course = None
        student = None
        allowed = False
        courseId = int(body.get("courseId"))
    
        try:
            course = Course.objects.get(id = courseId)
            
        except Course.DoesNotExist:
            pass

        try:
            student = User.objects.get(id = studentId)

        except User.DoesNotExist:
            pass
        try:
       
            group = CourseAccess.objects.get(course = course)
            
            if action == "remove":
               
                course.students.remove(student)
                allowed = False
                
            else:
                
                course.students.add(student)
                allowed = True
                
            group.save()
          
        except Course.DoesNotExist:
            print("group ",group.students.all())
            
            
     
            
        json_course = {
            'allowed':True if allowed else False
        }        
        return JsonResponse(json_course)
    
    
    
# from rest_framework.permissions import AllowAny

# class PasswordResetAPIView(views.APIView):
#     queryset = LmsUser.objects.all()
#     permission_classes = [AllowAny]

#     def post(self, reuest):
#         form = PasswordResetForm(request.data)
        
#         if form.is_valid():
#             form.save(request=request)
            
#             return Response({'detail': 'Password reset email has been sent.'}, status=status.HTTP_200_OK)
#         else:
#             return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
