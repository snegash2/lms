from braces.views import JsonRequestResponseMixin, CsrfExemptMixin
from django.apps import apps
from django.forms import modelform_factory,modelformset_factory
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.urls import reverse_lazy
from django.core.cache import cache
from students.forms import CourseEnrollForm
from .forms import ModuleFormSet
from .models import Course, Module, Content
from django.db.models import Count
from .models import Category
from django.views.generic.detail import DetailView
from django.shortcuts import render
from django.contrib.auth.models import Group,User
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
    fields = ['course_name', 'slug', 'overview','image']
    success_url = reverse_lazy('courses:manage_course_list')

class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = 'courses/manage/course/form.html'


class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'courses/manage/course/list.html'
    permission_required = 'courses.view_course'
    


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    permission_required = 'courses.add_course'



    
class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    permission_required = 'courses.change_course'

class ModuleContentListView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/content_list.html'

    def get(self, request, module_id):
        module = get_object_or_404(Module,
                                   id=module_id,
                                   course__teacher=request.user)
        return self.render_to_response({'module': module})


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses.delete_course'

class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/formset.html'
    course = None
    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course,data=data)


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
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('courses:manage_course_list')
        return self.render_to_response({
        'course': self.course,
        'formset': formset})



class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = 'courses/manage/content/form.html'

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
        context = super().get_context_data(**kwargs)

        context['enroll_form'] = CourseEnrollForm(
            initial={'course': self.object})
        return context


def verify_egiliable_student(request,id):
    # egiliable_students_group = Group.objects.get(name='can_take_exam')
    # egiliable_students = egiliable_students_group.user_set.all()
    group = Group.objects.get(name='can_take_exam')
    user_email = request.POST.get('user')
    if request.method == "POST":
       if request.POST.get('user-to-deny') != None:
            user = User.objects.get(email = user_email)
            user.groups.remove(group)
            user.save()
            


     
       user = User.objects.get(email = user_email)
       user.groups.add(group)
       user.save()
      


    course = Course.objects.get(id = id)

    candidate_students = course.students.all()
  
    context = {
        'course_id':id,
        'group_users':group.user_set.all(),
        'candidate_students':candidate_students
    }
    return render(request,'courses/course/egiliablity.html',context)