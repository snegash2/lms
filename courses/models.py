from io import BytesIO
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.template.loader import render_to_string
from courses.fields import OrderingField
from django.utils.translation import gettext as _
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.conf import settings
import uuid
from embed_video.fields import EmbedVideoField

# from django.contrib.auth.models import User
import re
from PIL import Image


User = get_user_model()
class Category(models.Model):

    category = models.CharField(
        verbose_name=_("Category"),
        max_length=250, blank=True,
        unique=True, null=True)
    # sub_categories = models.ManyToManyField("SubCategory",null = True,blank= True)
    courses = models.ManyToManyField("Course",related_name="courses",null= True,blank= True)
    slug = models.SlugField()

    def __str__(self):
        return f"{self.category}"




class CourseName(models.Model):
    
    name = models.CharField(max_length=200)
    category = models.ManyToManyField(Category,
                                verbose_name='Category',
                                related_name='categories',
                                # on_delete=models.CASCADE,
                                blank = True,
                                null = True,
                                default=None)



    def __str__(self):
        return self.name
    


class Note(models.Model):
    course = models.ForeignKey("Course",
                                verbose_name='noteCourse',
                                related_name='note_courses',
                                on_delete=models.CASCADE,
                                default=None)
    user   = models.ForeignKey(User,
                                verbose_name='User',
                                related_name='users',
                                on_delete=models.CASCADE,
                                default=None)
    
    content = models.TextField(blank = True,null = True)



    def __str__(self):
        return self.course.name + self.user.username
    
    
    
    
class Reference(models.Model):
    module = models.ForeignKey("Module",
                                verbose_name='Reference Module',
                                related_name='rmodules',
                                blank = True,
                                null = True,
                                on_delete=models.CASCADE,
                                default=None)

    
    files = models.FileField(upload_to= 'files',blank = True,null = True)
    link = models.URLField(blank = True,null = True)


    def __str__(self):
        return f"{self.module.title}"





class Course(models.Model):
    
    LEVEL_CHOICES = (
        ('BASIC', 'Basic'),
        ('INTERMEDIATE', 'Intermediate'),
        ('ADVANCED', 'Advanced'),
        ('EXPERT', 'Expert'),
        # Add more choices as needed...
    )
    
    Course_CHOICES = (
     
        ('PDF', 'PDF'),
        ('VIDEO', 'VIDEO'),
     
    )
    teacher = models.ForeignKey(User,
                                null=True,
                              related_name='courses_created',
                              on_delete=models.SET_NULL)
    # name = models.CharField("Course Name ",max_length=200)
    name    = models.ForeignKey(CourseName,on_delete = models.CASCADE)
    category = models.ForeignKey(Category,
                                verbose_name='Category',
                                related_name='names',
                                on_delete=models.CASCADE,
                                null = True,
                                blank = True)
    course_type = models.CharField(max_length=255, choices=Course_CHOICES, default='PDF')


    slug = models.SlugField(max_length=200, unique=False)


    # overview = RichTextUploadingField()
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(User,related_name='courses_joined',blank=True)
    image = models.ImageField(null = False,blank = False,upload_to='media/images',default="media/images/avatar.png")
    has_practice = models.BooleanField(default=False,null = True,blank = True)
    ceu          = models.IntegerField(default= 34)
    published   = models.BooleanField(default=False)
    reason_not_published = models.TextField(default="",blank = True,null= True,help_text = "Reason not published.")
    intro_video = EmbedVideoField()


    class Meta:
        ordering = ['-created']
        verbose_name = "Course"

    def __str__(self):
        return f"{self.slug}"
    
    @property
    def detail(self):
        return f"{self.overview[3:70]} ..."


    
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     self.slug = slugify(self.id)


   



class Module(models.Model):
    course = models.ForeignKey(Course,
                               related_name='modules',on_delete=models.CASCADE)
    title = models.CharField("Module Name:",max_length=200)
    description = models.TextField("Module Overview:",blank=True)
    order = OrderingField(blank=True, for_fields=['course'])
    # pdfs =  models.ManyToManyField("File",blank= True)
    def __str__(self):
        return f'{self.order}. {self.title}'

    class Meta:
        ordering = ['order']

    @property
    def detail(self):
        return f'{self.title[:10]}'



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
    
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL,
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
    file = models.FileField(upload_to='media/files')




# actually class to sotre image
class Image(GenericItem):
       file = models.FileField(upload_to='media/images')

class VideoManager(models.Manager):
    def get_queryset(self,model):
        return model.filter(name__endswith=".mp4")



# actually class to store url of video
class Video(GenericItem):
    video =  EmbedVideoField()
    # objects = VideoManager()



# actually Tasks
class Task(GenericItem):
    module = models.ForeignKey(Module,related_name = "tasks", on_delete=models.CASCADE)
    title = models.CharField(max_length= 255,blank = True,null = False)
    task   = models.TextField(max_length=255, blank = True, null =False)
    description = models.TextField(max_length=255, blank = True)

    def __str__(self):
        return f"{self.title}"





class CourseAccess(models.Model):
    name = models.CharField(max_length=255, blank = True)
    students = models.ManyToManyField(User)
    course = models.ForeignKey(Course,related_name = "course",null = True,blank = True,on_delete = models.CASCADE)
    
    
    
    def __str__(self):
        return f"{self.course}"