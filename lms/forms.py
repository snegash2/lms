from allauth.account.forms import SignupForm
from django.contrib.auth.models import User

from django import forms
from django.contrib.auth.forms import UserCreationForm


class LmsSignupForm(UserCreationForm):
    # Add any additional fields you want to your form here.
    ROLES = [
        ('admin', 'Admin'),
        ('student', 'Student'),
        ('instructor', 'Instructor'),
    ]

    roles = forms.ChoiceField(choices=ROLES, widget=forms.Select())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'roles')



