from django import forms
from django.forms.widgets import RadioSelect, Textarea
from .models import Quiz,Question,Sitting
from exam.multichoice.models import  Answer,MCQuestion
from courses.models import Course
from exam.quiz.models import Category,SubCategory
from exam.multichoice.models import MCQuestion,Answer
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import gettext_lazy as _
from django.forms.models import inlineformset_factory
from django.forms import TextInput, Textarea
from crudbuilder.formset import BaseInlineFormset

# QuestionFormSet = inlineformset_factory(MCQuestion,
#             Answer,
#             fields=['content',
#             'correct',],
#             #  widgets={
#             #         'content': TextInput(attrs={'class': 'form-control-lg','placeholder': 'Enter module title','style':'width:95%;margin-bottom:5px;'}),
#             #         'corre': Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Brief module description','style':'width:95%;'}),
#             #     },
#             extra=3,
#             max_num=105,
#             can_delete=True,

#             )

class ChildModelForm(forms.ModelForm):
    class Meta:
        model = MCQuestion
        fields = "__all__"
    answer_order = forms.CharField(label="Answer order",widget=forms.TextInput(attrs={'class':'form-select'}))


class QuestionFormSet(BaseInlineFormset):
    
        def __init__(self) -> None:
            print("Creating Question Form")
            super().__init__()
        inline_model = Answer
        parent_model = MCQuestion
        exclude = ['category', 'sub_category']
        extra = 4
        
     

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

        
        
 

