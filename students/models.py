from django.db import models
from django.contrib.auth.models import User



class Certification(models.Model):
    owner = models.ForeignKey(User, related_name="certifications",on_delete = models.CASCADE,null = True,blank = True)
    name = models.CharField(max_length=100)
    issuer = models.CharField(max_length=100)
    date_earned = models.DateField()

    def __str__(self):
        return self.name
    
    
  

class StudentActivity(models.Model):
    user = models.ForeignKey(User, related_name = "actvities",on_delete=models.CASCADE)
    activity = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.activity}"
    
    
    


class Profile(models.Model):
    user = models.OneToOneField(User, related_name = "profile",on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='media/avatars/', blank=True,default= "media/avatar/avatar.png")
    # Add any other fields you want to include in the profile model

    def __str__(self):
        return self.user.username
    
    
    
class GlobalSetting(models.Model):
     user = models.OneToOneField(User, related_name = "globals",on_delete=models.CASCADE)
     data_stored = models.JSONField(default=None)
     
     
     def __str__(self) -> str:
         return f"global setting of {self.user.username}"
    