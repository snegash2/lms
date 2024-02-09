from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from students.models import Profile
from landing.models import LmsUser





@receiver(post_save, sender=LmsUser)
def  profile_creator(sender, instance, created, **kwargs):
    # Perform actions when YourModel is saved
    if created:
        Profile.objects.create(user = instance)
        print("Object created:", instance)
