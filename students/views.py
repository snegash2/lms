from typing import Any
from django.db.models.query import QuerySet
from django.urls import reverse_lazy,resolve,reverse
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView,UpdateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
# from django.urls import reverse,redirect
from django.shortcuts import get_object_or_404,redirect
from courses.models import Course,Module,Assignment
from .forms import CourseEnrollForm,AssModalForm
from django.core.files.uploadedfile import InMemoryUploadedFile
from crendential.models import Crendential
from django.contrib.auth import get_user_model
from students.models import Certification,StudentActivity,Profile
from crendential.forms import CrendentialForm
from .forms import StudentProfile
from django.shortcuts import  render
from django.contrib import messages
from django.http import JsonResponse
from django.http import HttpResponseBadRequest, JsonResponse  # Use JsonResponse for JSON response

    # File: views.py
from bootstrap_datepicker_plus.widgets import DateTimePickerInput
from django.views import generic



User = get_user_model()
class StudentRegistrationView(CreateView):
    template_name = 'students/student/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('student_course_list')
    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'],
        # activity = StudentActivity.objects.create(user = self.request.user,activity = "Student Registred")
        # activity.save()
        password=cd['password1'])
        login(self.request, user)
        return result




class StudentDashboard(DetailView):
    model = User
    template_name = 'students/student/student_dashboard.html'

    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        course_nums = 0
        courses = Course.objects.all()
      
        
        for course in courses:
            students = course.students.all()
            if self.request.user in students:
                course_nums += 1
        context['course_nums'] = course_nums
        if self.request.user.is_authenticated:            
            context['certifications'] = self.request.user.certifications.count()
        actvities = self.request.user.actvities
        profile = self.request.user.profile
        if profile:
            context['profile'] = profile
          
        
        if actvities:
            context['actvities'] = actvities
    
      
            
        return context

class StudentEnrollCourseView(LoginRequiredMixin,FormView):
    course = None
    form_class = CourseEnrollForm
    template_name = "courses/course/detail.html"

    def post(self,request):
        user_id = request.POST.get("user")
        course_id   = request.POST.get("id")
        slug = request.POST.get("slug")
        course = get_object_or_404(Course,id = course_id)
        user = get_object_or_404(User,id = user_id)
        
        course.students.add(user)
        course.save()
        activity = StudentActivity.objects.create(user = self.request.user,activity = f"Student Enroled")
        activity.save()
        
        return redirect("courses:course_detail",slug = slug)


    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super().form_valid(form)
    
    
class StudentSubmitAss(LoginRequiredMixin,FormView):
    course = None
    form_class = CourseEnrollForm
    template_name = "courses/course/submit_ass.html"
    
    
  
    def get_context_data(self, **kwargs):
        crendentials = None
        context = super().get_context_data(**kwargs)
        id = None
        form = CrendentialForm()
 
        try:
            id = kwargs.get(id,None)
            module = Module.objects.all().last()
            # assiagnment = Assignment.objects.filter(module = module,course = self.request.user.courses_joined.all().first()).first()
            assiagnment = Assignment.objects.filter(module = module).first()

            context['module'] = module
            context['ass'] = assiagnment
            context['form'] = form
        except Module.DoesNotExist:
            pass

        return context
    
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        module = Module.objects.get(id = kwargs.get("id"))
        print("module ",module.course.id)

        form = CrendentialForm(request.POST, request.FILES)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.course = module.course
            instance.save()
            form.save()
            # Extract cleaned data from the form
            # cleaned_data = form.cleaned_data

            # # Create a new assignment instance with validated data
            # new_assignment = Assignment.objects.create(
            #     course=module.course,
            #     title=cleaned_data['title'],
            #     module=module,
            #     description=cleaned_data['description'],
            #     file=cleaned_data['file'],
            # )
            messages.success(self.request, 'you submit  assiagment success fully.')
            return redirect('students:submit-assiagnment', id= kwargs.get("id"))
        else:
            # Handle form validation errors
            return JsonResponse({'errors': form.errors}, status=400)  # Use status code for errors


 
    

    
    

    
class StudentDropoutCourseView(LoginRequiredMixin,FormView):
    course = None
    form_class = CourseEnrollForm
    template_name = "courses/course/detail.html"

    def post(self,request):
        user_id = request.POST.get("user")
        course_id   = request.POST.get("id")
        slug = request.POST.get("slug")
        course = get_object_or_404(Course,id = course_id)
        user = get_object_or_404(User,id = user_id)
        
        course.students.remove(user)
        course.save()
        activity = StudentActivity.objects.create(user = self.request.user,activity = f"Student Enroled")
        activity.save()
        
        return redirect("courses:course_detail",slug = slug)


    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.remove(self.request.user)
        return super().form_valid(form)


    # def get_success_url(self):
    #     return reverse_lazy('student_course_detail', args=[self.course.id])


class StudentCourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'students/course/list.html'
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])
    
    
    
class UploadProfilePic(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'students/course/list.html'
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])

class StudentCourseDetailView(DetailView):
    model = Course
    template_name = 'students/course/detail.html'

    def get_queryset(self):
        qs = super().get_queryset()
        if qs.filter(students__in=[self.request.user]) != None:
            qs = qs.filter(students__in=[self.request.user])

        else:
            raise ValueError("user is not registered for this course")
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # get course object
        course = self.get_object()
        if 'module_id' in self.kwargs:
            # get current module
            context['module'] = course.modules.get(
                id=self.kwargs['module_id'])
        else:
            if course.modules.all().exists():
                context['module'] = course.modules.all()[0]
            else:
                raise ValueError("not module for this course")

        return context


    def post(self, request, *args, **kwargs):
        user = request.user
        # name  = request.POST.get('name')
        file = request.FILES['fileInput']
        
        cr = Crendential.objects.filter(user = request.user)
        
        if not cr.exists():
            cr = Crendential()
            cr.user = user
            cr.file = file
            cr.save()
            messages.success(self.request, 'you uploaded crendentials success fully.')
            return redirect('students:student_course_detail', pk=self.get_object().id)
        
        else:
            cr = cr.first()
            cr.file = file
            cr.save()
            messages.success(self.request, 'you update  crendentials success fully.')
            return redirect('courses:course_detail', slug=self.get_object().slug)
        # return reverse('students:student_course_detail', args=[self.get_object().id])
        




    
class StudentProfileView(LoginRequiredMixin,UpdateView):
    
    
    form_class = StudentProfile
    model = Profile
    # fields = "bio","location","birth_date"
    template_name =  'students/student/student_dashboard.html'

    

        
        
    def get_form(self):
        form = super().get_form()
        form.fields["birth_date"].widget = DateTimePickerInput()
        return form
    
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        
    
        context =  super().get_context_data(**kwargs)
        course_nums = 0
        mycourses = self.request.user.courses_joined.all()
        print("courses ",mycourses)
        
        for course in mycourses:
            students = course.students.all()
            if self.request.user in students:
                course_nums += 1
        context['course_nums'] = course_nums
        if self.request.user.is_authenticated:            
            context['certifications'] = self.request.user.certifications.count()
        actvities = self.request.user.actvities
        profile = self.request.user.profile
        form = self.get_form()
        if profile:
            context['profile'] = profile
            context['form'] = form
            context['mycourses'] = mycourses
            context['courses'] = Course.objects.all()
          
        
        if actvities:
            context['actvities'] = actvities
            
        return context
    
    


    def get_success_url(self,**kwargs):
        messages.success(self.request, 'Profile update success fully.')
        return reverse_lazy('students:student_update_profile', args=[self.request.user.profile.pk])
    
    
    
    
