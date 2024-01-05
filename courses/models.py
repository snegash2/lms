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
from django.conf import settings
# from django.contrib.auth.models import User
import re
from PIL import Image


User = get_user_model()


    

class Category(models.Model):

    category = models.CharField(
        verbose_name=_("Category"),
        max_length=250, blank=True,
        unique=True, null=True)
    sub_categories = models.ManyToManyField("SubCategory")
    slug = models.SlugField()

    # objects = CategoryManager()

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return f"{self.category}"






class SubCategory(models.Model):

    name = models.CharField(
        verbose_name=_("Sub-Category"),
        max_length=250, blank=True, null=True)


    # objects = CategoryManager()

    class Meta:
        verbose_name = _("Sub-Category")
        verbose_name_plural = _("Sub-Categories")

    def __str__(self):
        return f"{self.name}" # + " (" + self.category.category + ")"



class CourseName(models.Model):
    name = models.CharField("Course Name ",max_length=200)
    category = models.ForeignKey(Category,
                                verbose_name='Category',
                                related_name='categories',
                                on_delete=models.CASCADE,
                                default=None)



    def __str__(self):
        return self.name



class Course(models.Model):

    # need user can delete course but course can't delete
    teacher = models.ForeignKey(User,
                                null=True,
                              related_name='courses_created',
                              on_delete=models.SET_NULL)
    name = models.CharField("Course Name ",max_length=200)
    category = models.ForeignKey(Category,
                                verbose_name='Category',
                                related_name='names',
                                on_delete=models.CASCADE,
                                null = True)
    # skill_level = models.CharField(choices)

    sub_category = models.ForeignKey(SubCategory,
                                verbose_name='Sub Category',
                                related_name='categories',
                                on_delete=models.CASCADE,
                                default=None)


    

    
    slug = models.SlugField(max_length=200, unique=True)

    overview = RichTextUploadingField()
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(User,related_name='courses_joined',blank=True)
    image = models.ImageField(null = True,blank = True,upload_to='images')
    has_practice = models.BooleanField(default=False)
    ceu          = models.IntegerField(default= 0)
    published   = models.BooleanField(default=False)
    reason_not_published = models.TextField(default="")


    class Meta:
        ordering = ['-created']
        verbose_name = "Course Content"

    def __str__(self):
        return f"{self.name}"
    
    @property
    def detail(self):
        return f"{self.overview[3:40]} ..."


    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.slug = slugify(self.name)


    # def save(self, *args, **kwargs):
    #     # Open the original image using PIL
    #     original_image = Image.open(self.image.path)

    #     # Set the desired size for the resized image
    #     resized_size = (800, 600)
    #     self.slug = slugify(self.course_name)
    #     # Resize the image
    #     original_image.thumbnail(resized_size)

    #     # Save the resized image back to the same field
    #     # Note: This will overwrite the original image file
    #     original_image.save(self.image.path)

    #     # Call the superclass's save() method to save the model
    #     super().save(*args, **kwargs)



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


