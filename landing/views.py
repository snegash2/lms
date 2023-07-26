from django.shortcuts import render
from courses.models import Course
from django.contrib.auth.models import Group,User



def landing_page(request):
    courses = Course.objects.filter(published = True)
    group = Group.objects.get(name='instructors')
    users = User.objects.all()
    instructors = group.user_set.count()
    user_num = users.count()
    student_num = int(user_num) - int(instructors)

    context = {
        'courses':courses,
        'instructors':instructors,
        'students_num':student_num
    }
    
    return render(request, 'landing/index.html',context)