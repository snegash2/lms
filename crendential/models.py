from django.db import models
from django.contrib.auth import get_user_model
from courses.models import Course



User = get_user_model()
def user_directory_path(instance, filename):
    return 'media/user_{0}/{1}'.format(instance.user.id, filename)

class Crendential(models.Model):
    user = models.ForeignKey(User, related_name = "student_document",on_delete = models.CASCADE)
    course = models.ForeignKey(Course, on_delete = models.CASCADE,default=1)
    title  = models.CharField(max_length=100,blank = True,null = True)
    description = models.CharField(max_length = 1000,blank = True,null = True)
    file = models.FileField(upload_to=user_directory_path)

    def __str__(self):
        return f'doc_{self.user.id}_{self.user.username}'

