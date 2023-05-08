from django.contrib.auth.views import LoginView
from accounts.forms import UserLoginForm


class MyLoginView(LoginView):
    authentication_form = UserLoginForm
