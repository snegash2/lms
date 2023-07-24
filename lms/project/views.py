from django.shortcuts import render
from django.contrib.auth.models import User
from allauth.account.views import SignupView



def index(request):
    return render(request, 'index.html')



class InstructorSignupView(SignupView):

    def get_form_kwargs(self, **kwargs):
        kwargs['fields'] = ['username', 'email', 'first_name', 'last_name']
        return kwargs

    def form_valid(self, form):
        user = form.save()
        # Do some custom processing here.
        return super().form_valid(form)

