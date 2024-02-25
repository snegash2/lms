from typing import Any, Mapping
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from django.forms.widgets import RadioSelect, Textarea
from .models import Quiz,Question,Sitting
from exam.multichoice.models import  Answer,MCQuestion
from courses.models import Course
from exam.quiz.models import Category,SubCategory
from exam.multichoice.models import MCQuestion,Answer
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import gettext_lazy as _
from django.forms.models import inlineformset_factory,modelformset_factory
from django.forms import TextInput, Textarea
from crudbuilder.formset import BaseInlineFormset


class MCAnswerForm(forms.ModelForm):
    ANSWER_ORDER_OPTIONS = (
    ('content', _('Content')),
    ('random', _('Random')),
    ('none', _('None'))
)
    class Meta:
        model = MCQuestion
        exclude = "category","sub_category"
    
    answer_order = forms.ChoiceField(label="Answer Order",choices=ANSWER_ORDER_OPTIONS,widget=forms.Select(attrs={'class':"form-select"}))
        
QuestionFormSet = inlineformset_factory(MCQuestion,
            Answer,
         
            form = MCAnswerForm,
             can_order=False,
            extra=3,
            can_delete=False,
            max_num=105,
            help_texts="Edit Question answers"

           )





class ChildModelForm(forms.ModelForm):
    class Meta:
        model = MCQuestion
        exclude = ('category',)


# class QuestionFormSet(forms.ModelForm):
#     request = None
    
#     def __init__(self, user, *args, **kwargs):
#         super(QuestionFormSet, self).__init__(*args, **kwargs)
#         self.fields['quiz'].queryset = Course.objects.filter(teacher=user)
    
    
    
#     class Meta:
#         model = Question
#         exclude= ('category','explanation','sub_category')
#     quiz = forms.ModelChoiceField(label ='Question', queryset=Quiz.objects.none(),widget=forms.HiddenInput(attrs={'class':'form-select'}))
#     content = forms.CharField(label ='Question', widget=forms.Textarea(attrs={"id":"questionInput"}))
#     # figure = forms.FileField(label ='Question', widget=forms.FileInput(attrs={"class":"form-control"}))
        

        
     

class QuizFormSet(BaseInlineFormset):

        inline_model = MCQuestion
        parent_model = Quiz
        exclude = ['category', 'sub_category']
        extra = 4
     
        
     
        
        
   



class QuestionForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        choice_list = [x for x in question.get_answers_list()]
        self.fields["answers"] = forms.ChoiceField(choices=choice_list,
                                                   widget=RadioSelect)


class EssayForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super(EssayForm, self).__init__(*args, **kwargs)
        self.fields["answers"] = forms.CharField(
            widget=Textarea(attrs={'style': 'width:100%'}))


class InstructorQuizEditViewForm(forms.ModelForm):
    def __init__(self,course_instance,*args, **kwargs):
        super(InstructorQuizEditViewForm, self).__init__(*args, **kwargs)
        print("course type ",course_instance)
        self.fields['course'].queryset = course_instance
    class Meta:
        model = Quiz
        fields = "__all__"
        
    course = forms.ModelChoiceField(label="Course", queryset=Course.objects.none(), widget=forms.Select(attrs={'class': "form-select"}))
    category = forms.CharField(label="Category",widget=forms.Select(attrs={'class':"form-control w-100"}))
    questions = forms.ModelMultipleChoiceField(
        queryset=Question.objects.all().select_subclasses(),
        required=False,
        label=_("Questions"),
        widget=FilteredSelectMultiple(
            verbose_name=_("Questions"),
            is_stacked=False))



class InstructorQuestionEditViewForm(forms.ModelForm):
    
    def __init__(self,*args, **kwargs):
        super(InstructorQuestionEditViewForm, self).__init__(*args, **kwargs)
       
        self.fields['category'].queryset = Category.objects.all()
        self.fields['sub_category'].queryset = SubCategory.objects.all()

    class Meta:
        model = MCQuestion
        fields = "__all__"
    
    
    category = forms.ModelChoiceField(label="Category",queryset=Category.objects.none(),widget=forms.Select(attrs={'class':"form-select"}))
    sub_category = forms.ModelChoiceField(label="Sub Category",queryset=SubCategory.objects.none(),widget=forms.Select(attrs={'class':"form-select"}))
    
    

    
class InstructorAnswerEditViewForm(forms.ModelForm):
    

    class Meta:
        model = Answer
        fields = "__all__"

        
        
 

