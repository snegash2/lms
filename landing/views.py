from django.shortcuts import render
from courses.models import Course,Category,CourseName
from django.contrib.auth.models import Group,User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from students.forms import CourseEnrollForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from students.models import GlobalSetting
from django.contrib import messages
import json
from django.contrib.auth.models import Group,Permission
from django.core import serializers


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

def landing_page(request):
    courses = Course.objects.filter(published = True)
    group = None
    instructors = None
 
    try:
        group = Group.objects.get(name='instructors')
    except Group.DoesNotExist:
        pass
    
    users = User.objects.all()
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
        'enroll_form': CourseEnrollForm
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
            
        messages.success(request,"Global setting updated successfully")
         
        return JsonResponse(data)
      
          
          
          
          
@require_POST
def verify_egiliable_student_ajax(request):
   
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        body = json.loads(request.body)
        studentId = int(body.get("studentId"))
       
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
            group = Group.objects.all().filter(name = f"{course.name} students access group").first()
            group.user_set.add(student)
            group.save()
          
        except Group.DoesNotExist:
            print("group ",group)
    
        if student in group.user_set.all():
            print(f"{student} in group")
            allowed = False
            group.user_set.remove(student)
            group.save()
            
        elif student not in  group.user_set.all():
            print(f"{student} not in group")
            allowed = True
            group.user_set.add(student)
            group.save()
        else:
            pass
            
            
        json_course = {
            'allowed':allowed
        }        
        return JsonResponse(json_course)