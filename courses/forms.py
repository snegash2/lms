from typing import Any
from django import forms
from django.forms.models import inlineformset_factory
from .models import Course, Module


ModuleFormSet = inlineformset_factory(Course,
Module,
fields=['title',
'description',],
extra=1,
can_delete=True)




class EgiabilityForm(forms.Form):
    file = forms.FileField(label='File')

    def clean_file(self):
        file = self.cleaned_data['file']
        if file.content_type == 'image/jpeg':
            return file
        else:
            raise forms.ValidationError('Only JPEG files are allowed.')
        
        
        

class CourseCreateForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = 'category','teacher','published','sub_category','students','reason_not_published','name','slug'
        
        
