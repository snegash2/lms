from allauth.account.forms import LoginForm,SignupForm
from django.urls import reverse_lazy
from allauth.account.views import LogoutView,LoginForm
from django import forms
from collections import OrderedDict
from django.urls import path
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.forms import PasswordResetForm




class LmsSignupForm(LoginForm):
    first_name = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder':'First name','class':"form-control"}))


def global_forms(request):
    sign_in_form = SignupForm()
    login_in_form = LmsSignupForm()
    context = {
        'sign_in_form':sign_in_form,
        'login_in_form':login_in_form
    }
    return context




class MyCustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Specify the desired order of fields
        # self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email Address'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm Password'})
        
        self.fields['username'].widget.attrs.update({'autofocus': True})
        self.fields['first_name'].widget.attrs.update({'autofocus': True})
        self.fields['last_name'].widget.attrs.update({'autofocus': True})
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

        self.fields = OrderedDict(
            (key, self.fields[key]) for key in [
                'first_name',
                'last_name',
                # 'username',
                'email',
                'password1',
                'password2',
            ]
        )
    first_name = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder':'First name','class':"form-control"}))
    last_name = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder':'Last name','class':"form-control"}))
    email = forms.EmailField(label= "", required=True,widget=forms.TextInput(attrs={'placeholder':'Email','class':"form-control"}))  # Make email required
    # username = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder':'Username','class':""}))
    password1 = forms.CharField(label="",widget=forms.PasswordInput(attrs={'class':"form-control w-100"}))
    password2 = forms.CharField(label="",widget=forms.PasswordInput(attrs={'class':"form-check-input form-check-label"}))





