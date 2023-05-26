from io import BytesIO

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.template.loader import render_to_string

from courses.fields import OrderingField
class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ['title']
        verbose_name = "Course Name"

    def __str__(self):
        return self.title


class Course(models.Model):

    # need user can delete course but course can't delete
    teacher = models.ForeignKey(User,
                                default = "mr Ermi",
                              related_name='courses_created',
                              on_delete=models.SET_DEFAULT)
    subject = models.ForeignKey(Subject,
                                verbose_name='Course Name',
                                related_name='courses',
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = RichTextUploadingField()
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(User,related_name='courses_joined',blank=True)
    image = models.ImageField(null = True,blank = True,upload_to='images')


    class Meta:
        ordering = ['-created']
        verbose_name = "Course Content"

    def __str__(self):
        return self.title



class Module(models.Model):
    course = models.ForeignKey(Course,
                               related_name='modules',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = RichTextUploadingField(blank=True)
    order = OrderingField(blank=True, for_fields=['course'])

    def __str__(self):
        return f'{self.order}. {self.title}'

    class Meta:
        ordering = ['order']



    def __str__(self):
        return f'{self.order}. {self.title}'


# Polymorphism is the provision of a single interface to entities of different types
class Content(models.Model):
    module = models.ForeignKey(Module,
                               related_name='contents',
                               on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE,limit_choices_to={'model__in':(
                                'text',
                                'video',
                                'image',
                                'file')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderingField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']


# abstract model which acts base as class for diffrent type content
class GenericItem(models.Model):
    teacher = models.ForeignKey(User,
                              related_name='%(class)s_related',
                              on_delete=models.CASCADE)
    title   = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def render(self):
        return render_to_string(
            f'courses/content/{self._meta.model_name}.html',
            {'item': self})

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

# actually class to store text
class Text(GenericItem):
    content = RichTextUploadingField()
    # content = models.TextField()


# actually class to store file
class File(GenericItem):
    file = models.FileField(upload_to='files')



# actually class to sotre image
class Image(GenericItem):
       file = models.FileField(upload_to='images')

class VideoManager(models.Manager):
    def get_queryset(self,model):
        return model.filter(name__endswith=".mp4")



# actually class to store url of video
class Video(GenericItem):
    url = models.URLField(blank=True,null=True)
    video = models.FileField(upload_to="couses/videos", blank=True, null=True, validators=[])
    # objects = VideoManager()


