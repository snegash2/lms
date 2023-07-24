from django.shortcuts import render
from django.contrib.auth.models import User,Group
from allauth.account.views import SignupView
from django.views import View
from django.dispatch import Signal


def index(request):
    return render(request, 'index.html')



class InstructorSignupView(SignupView):

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


