from django.db import models
from django.contrib.auth.models import AbstractUser



class LmsUser(AbstractUser):
    # Add your custom fields here
    # For example, let's add a new field called "phone_number"
    phone_number = models.CharField(max_length=20)
