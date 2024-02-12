from typing import Any
from django import forms
from django.forms.models import inlineformset_factory
from .models import Course, Module,Assignment
from django.forms import BaseInlineFormSet
from django.forms import TextInput, Textarea
from .views import *




ModuleFormSet = inlineformset_factory(Course,
Module,
fields=['title',
'description',],
 widgets={
        'title': TextInput(attrs={'class': 'form-control-lg','placeholder': 'Enter module title','style':'width:95%;margin-bottom:5px;'}),
        'description': Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Brief module description','style':'width:95%;'}),
    },
extra=3,
max_num=105,
can_delete=True,

)


class EgiabilityForm(forms.Form):
    file = forms.FileField(label='File')

    def clean_file(self):
        file = self.cleaned_data['file']
        if file.content_type == 'image/jpeg':
            return file
        else:
            raise forms.ValidationError('Only JPEG files are allowed.')
        
        
        
        
Course_CHOICES = (
     
        ('PDF', 'PDF'),
        ('VIDEO', 'VIDEO'),
     
    )


class CourseCreateForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = 'category','teacher','published','students','reason_not_published','slug','name',"ceu","has_practice"
        
    course_type = forms.ChoiceField(label="Course Type",choices=Course_CHOICES,widget=forms.Select(attrs={'class':"form-select"}))
    intro_video = forms.URLField(widget=forms.URLInput(attrs={'class':"form-control w-100",'placeholder':"Intro video"}))


class ModuleCreateForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = "title","description"


class CourseUpdateForm(forms.ModelForm):


    class Meta:
        model = Course
        exclude = 'category','teacher','published','students','reason_not_published','slug','name',"ceu","has_practice"
        
        
        course_type = forms.ChoiceField(label="Course Type",choices=Course_CHOICES,widget=forms.Select(attrs={'class':"form-select"}))
        ceu = forms.IntegerField(label="Credit Hourse",widget=forms.NumberInput(attrs={'class':"form-control w-100"}))
        has_practice = forms.BooleanField(label="Haspractice",widget=forms.CheckboxInput(attrs={'class':"form-check-input form-check-label"}))
        intro_video = forms.URLField(label= "You tube video",widget=forms.URLInput(attrs={'class':"form-control w-100"}))





# class AssiagmentForm(forms.ModelForm):


#     class Meta:
#         model = Assignment
#         fields = "__all__"
        
#     module = forms.ChoiceField(label="Module",choices=Course_CHOICES,widget=forms.Select(attrs={'class': "form-select"}))
        
        
        
        
class AssiagmentForm(forms.ModelForm):
    def __init__(self, course_instance, *args, **kwargs):
        super(AssiagmentForm, self).__init__(*args, **kwargs)
        self.fields['module'].queryset = Module.objects.filter(course=course_instance)

    module = forms.ModelChoiceField(label="Module", queryset=Module.objects.none(), widget=forms.Select(attrs={'class': "form-select"}))

    class Meta:
        model = Assignment
        fields = "__all__"