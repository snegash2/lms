from django.db import models
from django.contrib.auth.models import User
from courses.models import Course


def user_directory_path(instance, filename):
    return 'media/user_{0}/{1}'.format(instance.user.id, filename)

class Crendential(models.Model):
    user = models.ForeignKey(User, related_name = "student_documents", on_delete = models.CASCADE)
    course = models.ForeignKey(Course, on_delete = models.CASCADE, related_name = "crendentials" ,default=1)
    # name  = models.CharField(max_length=100)
    file = models.FileField(upload_to=user_directory_path)

    def __str__(self):
        return f'doc_{self.course.slug} of {self.user}'

