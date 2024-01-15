from django import forms
from tempus_dominus.widgets import DateTimePicker
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from students. models import Profile
from courses.models import Course



class CourseEnrollForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(),widget=forms.HiddenInput)
    
    
    
class StudentProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "bio","location","birth_date"
        
        
        
    birth_date = forms.DateTimeField(
        widget=DateTimePicker(
            options={
                'useCurrent': True,
                'collapse': False,
            },
            attrs={
                'append': 'fa fa-calendar',
                'input_toggle': False,
            }
        ),
        label='Select a date and time'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('datetime_field', css_class='datetimepicker-input'),
            Submit('submit', 'Submit')
        )
        
    
    