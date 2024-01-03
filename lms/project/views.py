from django.shortcuts import render
from django.contrib.auth.models import User,Group
from allauth.account.views import SignupView
from django.views import View
from django.dispatch import Signal


def index(request):
    courses = 5
    return render(request, 'index.html',{courses:courses})



class InstructorSignupView(SignupView):

    def get_context_data(self, **kwargs):
        ret = super(InstructorSignupView, self).get_context_data(**kwargs)
        # group = Group.objects.get(name='instructors')
        # ret.user.groups.add(group)
    
        return ret

    def dispatch(self, request,**kwargs):   
        # user = self.form_valid(request,**kwargs) 
        # print("hell world is this user ",user)
        print(kwargs)
      
        return super().dispatch(request,**kwargs)
  
    def form_valid(self, form):
        print("hell save method is calling")
        user = form.save()
        user.save()
        group = Group.objects.get(name='instructors')
        user.groups.add(group)
        return super().form_valid(form)


    def get_success_url(self,request,**kwargs):
        user = request.user
        group = Group.objects.get(name='instructors')
        user.groups.add(group)
        return super().get_success_url(request,**kwargs)


