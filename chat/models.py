from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
    user    = models.ForeignKey(User, on_delete = models.CASCADE)
    course  = models.ForeignKey("courses.Course", on_delete = models.CASCADE,default=1)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_created=True,auto_now=False)
    updated_at = models.DateTimeField(auto_created=False,auto_now=True)

    def __str__(self):
        return f"{self.user.username}"