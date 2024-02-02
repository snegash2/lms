from typing import Any
from django import forms
from django.forms.models import inlineformset_factory
from .models import Course, Module
from django.forms import BaseInlineFormSet
from django.forms import TextInput
from django.forms import TextInput, Textarea




ModuleFormSet = inlineformset_factory(Course,
Module,
fields=['title',
'description',],
 widgets={
        'title': TextInput(attrs={'class': 'form-control col-12 mb-4', 'placeholder': 'Enter module title', "style":"margin-bottom: 10px;width:auto;"}),
        'description': Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Brief module description'}),
    },
extra=3,
can_delete=False
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
    ceu = forms.IntegerField(label="Credit Hourse",widget=forms.NumberInput(attrs={'class':"form-control w-100"}))
    has_practice = forms.BooleanField(label="Haspractice",widget=forms.CheckboxInput(attrs={'class':"form-check-input form-check-label"}))
    intro_video = forms.URLField(label= "You tube video",widget=forms.URLInput(attrs={'class':"form-control w-100"}))
    # overview = forms.Textarea("Course Overview",widget=forms.TextInput(attrs={'class':"form-control w-100"}))


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

