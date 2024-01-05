from django.shortcuts import render
from courses.models import Course,SubCategory,Category,CourseName
from django.contrib.auth.models import Group,User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from students.forms import CourseEnrollForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json



@require_POST
def enroll_form(request):
    pass
    


@require_POST
def filter_courses(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        category = None
        # Filter the courses based on the category
        
        category = json.loads(request.body)

        try:
          
            if category.get('category') == "All":
                courses = Course.objects.all()
            else:
                category = Category.objects.get(category=category.get('category'))
                courses = Course.objects.filter(category=category)

        except Category.DoesNotExist:
            raise ValueError("Category ")
        # Prepare the data to be sent as JSON
        courses_dict = []
        for course in courses:
            data = {
                "id":course.id,
                "name" : course.name,
                "slug": course.slug,
                'image_url':course.image.url,
                'detail':course.detail
                # 'students':[student for student in course.students.all],

            }
            courses_dict.append(data)
        data = {
            'courses': courses_dict
           
        }

        return JsonResponse(data)

def landing_page(request):
    courses = Course.objects.filter(published = True)
  
    group = Group.objects.get(name='instructors')
    users = User.objects.all()
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