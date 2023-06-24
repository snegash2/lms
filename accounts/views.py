from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from accounts.forms import UserLoginForm,UserRegistrationForm,UserEditForm, ProfileEditForm
from django.shortcuts import render,redirect
from django.urls import resolve
from django.contrib import messages
from .models import Profile


def register(request):
    # user_form = None
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            Profile.objects.create(user=new_user)
            
            return render(request,'accounts/register_done.html',{'new_user': new_user})

    else:
        user_form = UserRegistrationForm()
    return render(request,'accounts/register.html',{'user_form': user_form})



@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,data=request.POST,files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
            # return redirect(resolve('courses:mine'))
        else:
            messages.error(request, 'Error updating your profile')

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,'accounts/edit.html',{'user_form': user_form,'profile_form': profile_form})