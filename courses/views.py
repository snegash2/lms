from typing import Any
from braces.views import JsonRequestResponseMixin, CsrfExemptMixin
from django.apps import apps
from django.forms import modelform_factory,modelformset_factory
from django.forms.models import BaseModelForm
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.urls import reverse_lazy
from django.core.cache import cache
from students.forms import CourseEnrollForm
from .forms import ModuleFormSet,CourseCreateForm,CourseUpdateForm,ModuleCreateForm,AssiagmentForm
from .models import Course, Module, Content,Category,CourseAccess
from django.db.models import Count
from .models import Category,CourseName,Assignment
from django.views.generic.detail import DetailView
from django.shortcuts import HttpResponse as HttpResponse, render,get_object_or_404,HttpResponse
from django.contrib.auth.models import Group,User
from crendential.models import Crendential
from django.utils.text import slugify
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import messages
from students.models import GlobalSetting
from django.views.decorators.http import require_POST
import json
import random
from django.core import serializers



# common behavior for all classes this class return courses which create only by currently logedin user
class OwnerMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(teacher=self.request.user)


# assign currently logedin user during editing of course
class OwnerEditMixin:
    def form_valid(self, form):
        form.instance.teacher = self.request.user
        return super().form_valid(form)


class OwnerCourseMixin(OwnerMixin,LoginRequiredMixin,PermissionRequiredMixin):
    model = Course
    # fields = ['category', 'slug', 'overview','image']
    success_url = reverse_lazy('courses:course_create')

class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    # template_name = 'courses/manage/course/form.html'
    template_name = 'courses/manage/course/AddInstructor.html'


class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'courses/manage/course/list.html'
    permission_required = 'courses.view_course'
    


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    permission_required = 'courses.add_course'
    form_class = CourseCreateForm
    

    
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        try:
            mycourses = Course.objects.filter(teacher =self.request.user)
        
        except Course.DoesNotExist:
            raise ValueError("Course Does not Exist")
        
        try:
            categories = Category.objects.all()
            
        except Category.DoesNotExist:
            raise context.clear()
        
        context['categories'] = categories
        context['mycourses'] = mycourses
        
        return context
    

    
        
    def post(self, request, *args, **kwargs):
        body = request.POST
        file = request.FILES
        form = CourseCreateForm(body,file)
        try:
            category = Category.objects.get(category =request.session.get('category')['category'] )
            setting  = GlobalSetting.objects.get(user = request.user)
            name = CourseName.objects.filter(name = setting.data_stored['value']).first()
        except Category.DoesNotExist:
            raise ValueError("No category is choice")
        if form.is_valid():
                subcategory = self.request.POST.get("courseName")
                form = form.save(commit=False) 
                form.slug = slugify(f"{form.overview[1::20] + str(random.randint(1,10000000))}")
                form.teacher = self.request.user
                form.category  = category
                form.name = name
                form.save()
                # messages.success(self.request, 'you added course success fully.')
                data = []
                forms = vars(form)
                json_data = serializers.serialize('json', [form])
                return JsonResponse({"response":json_data})

        return HttpResponse("not created")
    
    
  
    
class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    form_class = CourseCreateForm
    permission_required = 'courses.change_course'
    template_name = 'courses/manage/course/update_course.html'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['course'] = self.get_object()
        return context
    
    

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        data = {
            'success': True,
            'message': 'Object updated successfully.',
            'data': {
                'id': self.object.id,
                'name': self.object.slug,
                # Include other fields as needed
            }
        }
        return JsonResponse(data)

    def form_invalid(self, form):
        data = {
            'success': False,
            'message': 'Form is invalid.',
            'errors': form.errors
        }
        return JsonResponse(data, status=400)

    
    
    
    


class ModuleContentListView(TemplateResponseMixin, View):
    
    template_name = 'courses/manage/module/MainCourses.html'

    def get(self, request, module_id):
        module = get_object_or_404(Module,
                                   id=module_id,
                                   course__teacher=request.user)
        return self.render_to_response({'module': module})


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses.delete_course'
    
    


class CourseModuleUpdateView(TemplateResponseMixin, View):
    # template_name = 'courses/manage/module/formset.html'
    template_name = 'courses/manage/module/module.html'
    course = None
    
    def get_formset(self, data=None):
        formset = ModuleFormSet(instance=self.course,data=data)
        return formset
        
 


    def dispatch(self, request, pk):

        self.course = get_object_or_404(Course,
        id=pk,
        teacher=request.user)
        return super().dispatch(request, pk)


    def get(self, request, *args, **kwargs): 
        formset = self.get_formset()
        
        
        return self.render_to_response({
        'course': self.course,'formset': formset})


    def post(self, request, *args, **kwargs):
        if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            formset = self.get_formset(data=request.POST)
            if formset.is_valid():
                return JsonResponse({"course": self.course})
        
        
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            redirect('courses:manage_course_list')
     
        return self.render_to_response({
        'course': self.course,
        'formset': formset})





class ModuleAddView(CreateView):
    template_name = 'courses/manage/module/module.html' 
    
    permission_required = 'courses.add_course'
    form_class = ModuleCreateForm
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        
        try:
            course = Course.objects.get(pk = kwargs.get("pk"))
            self.course = course            
        except Course.DoesNotExist as e:
            raise e
        
        return context

        
    def post(self, request, *args, **kwargs):
        body = request.POST
        form = ModuleCreateForm(body)
        

        if form.is_valid():
                form = form.save(commit= False)
                form.course = self.course
                form.save()
                json_data = serializers.serialize('json', [form])
                return JsonResponse({"response":json_data})
     
        json_error = serializers.serialize('json', [form.errors])
        return JsonResponse({"response":json_error})
     
    
    
    
    
class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = 'courses/manage/content/content_form.html'

    def get_model(self, model_name):
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='courses',
                                  model_name=model_name)
        return None

    def get_form(self, model, *args, **kwargs):
        Form = modelform_factory(model, exclude=[
                                                 'teacher',
                                                 'order',
                                                 'created',
                                                 'updated'])
        return Form(*args, **kwargs)

    def dispatch(self, request, module_id, model_name, id=None):
        self.module = get_object_or_404(Module,
                                       id=module_id,
                                       course__teacher=request.user)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model,
                                         id=id,
                                         teacher=request.user)
        return super().dispatch(request, module_id, model_name, id)

    def get(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form': form,
                                        'object': self.obj})

    def post(self, request, module_id, model_name, id=None):
        form = self.get_form(self.model,
                             instance=self.obj,
                             data=request.POST,
                             files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.teacher = request.user
            obj.save()
            if not id:
                # new content
                Content.objects.create(module=self.module,item=obj)
            return redirect('courses:module_content_list', self.module.id)
        return self.render_to_response({'form': form,
                                        'object': self.obj})



class ContentDeleteView(View):
    def post(self, request, id):
        content = get_object_or_404(Content,id=id,module__course__teacher=request.user)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('courses:module_content_list', module.id)


class ModuleOrderView(CsrfExemptMixin,JsonRequestResponseMixin,View):
    def post(self, request):
        for id, order in self.request_json.items():
            Module.objects.filter(id=id,course__teacher=request.user).update(order=order)
        return self.render_json_response({'saved': 'OK'})


class ContentOrderView(CsrfExemptMixin,JsonRequestResponseMixin,View):
    def post(self, request):
        for id, order in self.request_json.items():
            Content.objects.filter(id=id,module__course__teacher=request.user) .update(order=order)
        return self.render_json_response({'saved': 'OK'})




class CourseListView(TemplateResponseMixin, View):
    model = Course
    template_name = 'courses/course/list.html'
    def get(self, request, category=None):

        categories = cache.get('all_categories')
        if not categories:
            categories = Category.objects.annotate(
            total_courses=Count('categories'))
        cache.set('all_categories', categories)



        courses = Course.objects.annotate(total_modules=Count('modules'))
        if category:
            category = get_object_or_404(Category, slug=category)
            key = f'category_{category.id}_courses'
            all_courses = cache.get(key)
            if not courses:
                courses = all_courses.filter(category=category)
                cache.set(key, courses)
            else:
                courses = cache.get('all_courses')
            if not courses:
                courses = all_courses
                cache.set('all_courses', courses)
        return self.render_to_response({'categories': categories,'category': category,'courses': courses})




class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course/detail.html'

    def get_context_data(self, **kwargs):
        crendentials = None
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            crendentials =  Crendential.objects.filter(course = self.object,user = self.request.user).first()
         
     
        context['enroll_form'] = CourseEnrollForm(
            initial={'course': self.object})
        
        context['course'] =  self.object
        if crendentials:
            context['crendentials'] = crendentials

        return context
    
    
    def post(self,request,**kwargs):
        user = request.user
        course = self.get_object()
        file = request.FILES.get('fileInput')
        crendential = Crendential.objects.create(user = user,course= course,file = file)
        print("crendentail ",crendential)
        if crendential:
            return JsonResponse({
                "success":True
            })
            
        else:
            return JsonResponse({
                "success":False
            })
            


def verify_egiliable_student(request,id):
    group = None

    try:
        course = Course.objects.get(id = id)
        docs =  Crendential.objects.filter(course = course)
        group = CourseAccess.objects.get(course = course)
        
    except:
        pass
    
    
    course_students = course.students.all()
    access_students = group.students.all()
    form = AssiagmentForm(course)

    context = {
        'course':course,
        'course_id':id,
        'group_users':group.students.all(),
        'candidate_students':course_students,
        'allowed_students' : access_students,
        'docs':docs,
        'num_docs':docs.count(),
        'form':form
    }
    return render(request,'courses/course/StudentList.html',context)



def view_egiliable_detail(request,id):
    user = User.objects.get(id = id)
    crendential = get_object_or_404(Crendential,user = user)
    
    context = {
        'crendential':crendential,
        'user':user
    }
    return render(request,'courses/course/egiliablity_detail.html',context)

def course_filter(request,category,subcategory):
    print("Category filter selected ",category,subcategory)
    courses = Course.objects.filter(published = True).filter(sub_category__name__icontains = subcategory)

    categories = Category.objects.all()


    context = {
        'courses':courses,
        'categories':categories
    }
    
    return render(request, 'landing/index.html',context)







@require_POST
def verify_egiliable_student_ajax(request):
   
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
   
        studentId = json.loads(request.body)
        print("studentId ",studentId)
        return JsonResponse({
            "studentId": studentId
        })
        
        
        

@require_POST
def delete_module(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        body =  json.loads(request.body)
        module_id = int(body['module_id'])
        course_id = int(body['course_id'])
        course = Course.objects.get(id = course_id)
        module = Module.objects.get(id = module_id,course = course)
        beforeDelete = module
        module.delete()
        return JsonResponse({
            "module": "success"
        })
        
        
# @require_POST
# def delete_delete(request):
#     if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
#         body =  json.loads(request.body)
#         module_id = int(body['module_id'])
#         course_id = int(body['course_id'])
#         course = Course.objects.get(id = course_id)
#         module = Module.objects.get(id = module_id,course = course)
#         beforeDelete = module
#         module.delete()
#         return JsonResponse({
#             "module": "success"
#         })
        
        
def delete_doc(request,id):
    doc = get_object_or_404(Crendential, pk=id)  
    group = None
    course = None

  
    try:
        # course = Course.objects.get(id = id)
        docs =  Crendential.objects.filter(course = course)
        # group = CourseAccess.objects.get(course = course)
        
    except:
        pass
    
    
    # course_students = course.students.all()
    # access_students = group.students.all()

    context = {
        'course':course,
        'course_id':id,
        # 'group_users':group.students.all(),
        # 'candidate_students':course_students,
        # 'allowed_students' : access_students,
        'docs':docs,
        'num_docs':docs.count()
    }# Replace 'Document' with your model name
    if request.method == 'GET':
        
        return render(request,'courses/course/StudentList.html',context)

    if request.method == 'POST':
        doc.delete()
        return JsonResponse({
            "delete":True})  # Redirect to a success page




class AssCreateView(CreateView):
    permission_required = 'courses.add_course'
    form_class = AssiagmentForm

    def post(self, request, *args, **kwargs):
        body = request.POST
        title = body.get('title')
        description = body.get('description')
        module_id = body.get('module')
        file = request.FILES.get('file')
        if file:
           ass = Assignment.objects.create(title = title,description = description,module = Module.objects.get(id = module_id))
           ass.file = file
           ass.save()
           
           return JsonResponse({"response":"OK"})
        return JsonResponse({"response":"no file "})