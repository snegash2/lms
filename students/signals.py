from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from students.models import Profile
from landing.models import LmsUser
from django.dispatch import receiver
from allauth.account.signals import user_logged_in
from django.shortcuts import redirect,HttpResponseRedirect




@receiver(post_save, sender=LmsUser)
def  profile_creator(sender, instance, created, **kwargs):
    # Perform actions when YourModel is saved
    if created:
        Profile.objects.create(user = instance)
        print("Object created:", instance)



# @receiver(user_logged_in)
# def redirect_by_role(request, user, **kwargs):
    
#     if user.role == "STUDENT":
#         return HttpResponseRedirect('/course/create/')  # Redirect to page
    
#     elif user.role == 'INSTRUCTOR':
#         print(user.role," role")
#         return HttpResponseRedirect('/course/create/')

#     else:
#         return redirect('xxx')  # Redirect to user profile

