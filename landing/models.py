from django.db import models
from django.contrib.auth.models import AbstractUser



class LmsUser(AbstractUser):
    # Add your custom fields here
    # For example, let's add a new field called "phone_number"
    ROLE_CHOICES = (
     
        ('STUDENT', 'STUDENT'),
        ('INSTRUCTOR', 'INSTRUCTOR'),
     
    )
    phone_number = models.CharField(max_length=20)
    role = models.CharField("Role",max_length=255, choices=ROLE_CHOICES, default='PDF')
