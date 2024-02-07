from allauth.account.forms import LoginForm,SignupForm
from django.urls import reverse_lazy
from allauth.account.views import LogoutView



def global_forms(request):
    sign_in_form = SignupForm()
    login_in_form = LoginForm()
    context = {
        'sign_in_form':sign_in_form,
        'login_in_form':login_in_form
    }
    return context