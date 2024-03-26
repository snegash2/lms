from django import forms
from tempus_dominus.widgets import DateTimePicker
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from students. models import Profile,Certification
from courses.models import Course,Assignment



class CourseEnrollForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(),widget=forms.HiddenInput)
    
    
    
class AssModalForm(forms.ModelForm):
            
    class Meta:
        model = Assignment
        fields = 'title','description','file'
    title = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control','style':'width:455px;'}))
    
    


class StudentProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields ="bio","location","birth_date"
        
        
    bio = forms.CharField(widget =forms.TextInput(attrs={'class':'form-control','row':23}))
    location = forms.CharField(widget =forms.TextInput(attrs={'class':'form-control','row':23}))
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
        
    
    