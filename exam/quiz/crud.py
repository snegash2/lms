from crudbuilder.abstract import BaseCrudBuilder
from .models import Quiz,Question
from .admin import QuizAdminForm
from .forms import QuestionFormSet,QuizFormSet
from exam.multichoice.models import MCQuestion
from exam.quiz.models import Quiz as myquiz

class Quiz(BaseCrudBuilder):
    model = Quiz
    search_fields = ['course']
    tables2_fields = ('course','description')
    tables2_css_class = "table table-bordered table-condensed"
    tables2_pagination = 20  # default is 10
    # inlineformset  = QuizFormSet
    login_required=True
    permission_required=True

    @classmethod
    def custom_queryset(cls, request, **kwargs):
        """Define your own custom queryset for list view"""
        qset = cls.model.objects.filter(course__teacher = request.user)
        return qset

    @classmethod
    def custom_context(cls, request, context, **kwargs):
        """Define your own custom context for list view"""
        context['custom_data'] = "Some custom data"
        
        return context

    # permissions = {
    #     'list': 'example.person_list',
    #     'create': 'example.person_create'
    # }
    # createupdate_forms = {
    #     'create': PersonCreateForm,
    #     'update': PersonUpdateForm
    # }
    
    
    
    
    
class MCQuestion(BaseCrudBuilder):
    model = MCQuestion
    search_fields = ['quiz']
    tables2_fields = ('quiz', 'content','explanation')
    tables2_css_class = "table table-bordered table-condensed"
    tables2_pagination = 20  # default is 10
    inlineformset  = QuestionFormSet
    modelform_excludes = ['explanation','figure','category','sub_category']
    login_required=True
    permission_required=True

    @classmethod
    def custom_queryset(cls, request, **kwargs):
        """Define your own custom queryset for list view"""
        qset = cls.model.objects.filter(quiz__course = request.user.courses_created.first())
        return qset

    @classmethod
    def custom_context(cls, request, context, **kwargs):
        """Define your own custom context for list view"""
        request.session['course_id'] = 1
        question = context['table_objects']
        
        context['custom_data'] = "Some custom data"
        return context
    
 
    
    custom_templates = {
        #'list': 'quiz/your_list_template.html',
        'create': 'instructor/quiz/edit_question.html',
        #'detail': 'quiz/your_detail_template.html',
        #'update': 'quiz/your_update_template.html',
        #'delete': 'auiz/your_delete_template.html'
        }