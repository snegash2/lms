import random

from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, TemplateView, FormView,CreateView,DeleteView,UpdateView
from courses.models import Course
from .forms import QuestionForm, EssayForm,InstructorAnswerEditViewForm,InstructorQuizEditViewForm,InstructorQuestionEditViewForm,QuestionFormSet,MCAnswerForm
from .models import Quiz, Category, Progress, Sitting, Question
from exam.essay.models import Essay_Question
from exam.multichoice.models import MCQuestion,Answer
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin
from django.views.generic.base import TemplateResponseMixin, View
from django.urls import reverse,resolve
from django.shortcuts import redirect
from django.http import JsonResponse
import json
from django.core.paginator import Paginator
from urllib.parse import urlencode



class InstructorQuestionEditView(LoginRequiredMixin,CreateView):
    model = MCQuestion
    # fields = "__all__"
  
    form_class = QuestionFormSet
    template_name = "instructor/quiz/edit_question.html"
    success_url = '/'
    

        
    def post(self, request: HttpRequest, *args: str, **kwargs) -> HttpResponse:
        pk = kwargs.get("pk")
        figure = request.FILES.get('figure')
        course = get_object_or_404(Course,pk = request.GET.get('q'))
        self.request.session['question_pk'] = pk
        LETTERS = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P']
        quiz = Quiz.objects.get(course = course)
        question_data = request.POST.get("question")
        question = MCQuestion.objects.create(answer_order = "random",figure = figure,content = question_data)
        question.quiz.add(quiz)
        for letter in LETTERS:
            choice = request.POST.get(f"choice_{letter}")
            correct = True  if request.POST.get(f'checkbox_{letter}') == "on"  else False
            if choice:
                answer = Answer.objects.create(question = question,content = choice,correct = correct)
                answer.save()
                
                url_name = 'list-question'
                q_value = pk
                url = reverse(url_name)

        return redirect(url_name)
    
    
    def get(self, request: HttpRequest, *args: str, **kwargs) -> HttpResponse:

        course = get_object_or_404(Course,pk = request.GET.get('q'))
        quiz = Quiz.objects.get(course = course)
        
        request.session['quiz_id'] = quiz.id
        context = {
            
            'quiz':quiz,
            'course':course,
            'course_id':course.id
            
        }
        return render(request,"instructor/quiz/edit_question.html",context )
    
    
    
    
class InstructorListEditView(LoginRequiredMixin,ListView):
    model = MCQuestion
 

    template_name ="instructor/quiz/question_detail.html"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        quiz = None
        course = None
        if self.request.GET.get('q'):
            course_id = self.request.GET.get('q')
            try:
                course = Course.objects.get(id = course_id)
            except Course.DoesNotExist:
                pass
            quiz  = Quiz.objects.get(course = course)
            self.request.session['quiz_id'] = quiz.id
        else:
            quiz_id = self.request.session.get('quiz_id')
            quiz = Quiz.objects.get(id = quiz_id)
            
            
        context['question'] = quiz.get_questions()
        context['question_pk'] = self.request.session.get('quiz_id')
        context['course_id'] =  self.request.GET.get('q')
        return context
    
    
    
    
@login_required
def InstructorUpdateEditView(request):
    
    id  = request.GET.get('q')
    question = MCQuestion.objects.get(id = id)
    LETTERS = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P'] 
    
    if request.method == 'POST':
     
        print("id ",id)
        print("data ",request.POST)
        print("question ",question)
        question_content = question.content
        question.content = request.POST.get("question")
        figure = request.FILES.get('figure')
        
        for answer,letter in zip(question.get_answers(),LETTERS):
            choice = request.POST.get(f"choice_{letter}")
            correct = True  if request.POST.get(f'checkbox_{letter}') == "on"  else False
            print("correct ",request.POST.get(f'checkbox_{letter}'))
            answer.content = choice
            answer.correct = correct
            answer.figure = figure
            answer.save()
            question.save()
        question.save()
        return redirect(reverse('list-question'))
    

    

    data = {
        'content':question.content,
        'answers':question.get_answers(),
        'figure':question.figure
        
    }
    context = {
    
        'id':id,
        "data":data,
        'question_content':question.content
    }
    return render(request,"instructor/quiz/update_question.html",context)
    
 
    
@login_required
def InstructorUpdateContentEditView(request):
    
    id  = request.GET.get('q')
    question = MCQuestion.objects.get(id = id)
    form = MCAnswerForm(instance=question)
 
    if request.method == 'POST':
        form = MCAnswerForm(request.POST or None,instance=question)
        
        if form.is_valid():
            form.save()
       
        return redirect(reverse('list-question'))
    context = {
        'form':form,
        'id':id
    }
    return render(request,"instructor/quiz/update_question_content.html",context)
    
  
    
    
    
class InstructorListSearchView(LoginRequiredMixin,ListView):
    model = MCQuestion
    paginate_by = 2
    template_name ="instructor/quiz/question_detail.html"
    
    
    def get_queryset(self):
        quryset =  super().get_queryset()
        search_query = self.request.GET.get('q')
        qs =  quryset.filter(content__contains = search_query)
        print("qs",qs)
        return qs
    

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        quiz_id = self.request.session.get('quiz_id')
        quiz = Quiz.objects.get(id = quiz_id)
    
        context['question'] = quiz.get_questions()
        context['question_pk'] = self.request.session.get('question_pk')
        return context
    
    
    
    
@login_required
def InstructorListDeleteView(request):
    body = json.loads(request.body)
    id = body['id']
    question = MCQuestion.objects.get(id = id)
    question.delete()
    return HttpResponse("Deleted")
    
   


    
class InstructorAnswerEditView(CreateView):
    model = Answer
    form_class = InstructorAnswerEditViewForm
    template_name = "instructor/quiz/edit_answer.html"
    success_url = '/'
    
    
    
    
    
class InstructorDeleteView(CreateView):
    model = MCQuestion
    form_class = InstructorAnswerEditViewForm
    template_name = "instructor/quiz/edit_answer.html"
    success_url = '/'
    

    

class InstructorQuizEditView(CreateView):
    model = Quiz
    form_class = InstructorQuizEditViewForm
    template_name = "instructor/quiz/edit.html"
    
    success_url = '/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the specific course instance based on URL parameter, ID, etc.
        course_instance = get_object_or_404(Course, pk=self.kwargs.get('pk'))
        course_instance = Course.objects.all()
        context['form'] = InstructorQuizEditViewForm(course_instance=course_instance)
        return context
    
    def get(self, request: HttpRequest, *args: str, **kwargs) -> HttpResponse:
        course_instance = Course.objects.filter(teacher = request.user)
        context = {
            'form':InstructorQuizEditViewForm(course_instance=course_instance)
        }
        return render(request,"instructor/quiz/edit.html",context)
    
    
    def post(self, request: HttpRequest, *args: str, **kwargs: random) -> HttpResponse:
        course_instance = Course.objects.filter(teacher = request.user)
        # print("data ",request.POST)
        # quiz = Quiz()
        # quiz.course = Course.objects.get(id = request.POST.get("course"))
        # quiz.title = request.POST.get("title")
        # quiz.description = request.POST.get("description")
        # quiz.url = request.POST.get("url")
        # quiz.random_order = request.POST.get("random_order")
        # quiz.max_questions = request.POST.get("max_questions")
        # quiz.answers_at_end = request.POST.get("answers_at_end")
        # quiz.pass_mark = request.POST.get("pass_mark")
        # quiz.success_text = request.POST.get("success_text")
        # quiz.fail_text = request.POST.get("fail_text")
        # quiz.save()
        
        form = InstructorQuizEditViewForm(request.POST)
        
        context = {
            'form':InstructorQuizEditViewForm(course_instance=course_instance)
        }
        return render(request,"instructor/quiz/edit.html",context)

    




class QuizMarkerMixin(object):
    @method_decorator(login_required)
    @method_decorator(permission_required('quiz.view_sittings'))
    def dispatch(self, *args, **kwargs):
        return super(QuizMarkerMixin, self).dispatch(*args, **kwargs)


class SittingFilterTitleMixin(object):
    def get_queryset(self):
        queryset = super(SittingFilterTitleMixin, self).get_queryset()
        quiz_filter = self.request.GET.get('quiz_filter')
        if quiz_filter:
            queryset = queryset.filter(quiz__title__icontains=quiz_filter)

        return queryset

# @permission_required("blog.view_post")
class QuizListView(PermissionRequiredMixin,ListView):
    model = Quiz
    permission_required ='quiz.view_quiz'

    def get_queryset(self):
        queryset = super(QuizListView, self).get_queryset()
        return queryset.filter(draft=False)

# @permission_required("exam.view_exam")
class QuizDetailView(DetailView):
    model = Quiz
    slug_field = 'url'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.draft and not request.user.has_perm('quiz.change_quiz'):
            raise PermissionDenied

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

# @permission_required("exam.view_exam")
class CategoriesListView(ListView):
    model = Category

# @permission_required("exam.view_exam")
class ViewQuizListByCategory(ListView):
    model = Quiz
    template_name = 'view_quiz_category.html'

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(
            Category,
            category=self.kwargs['category_name']
        )

        return super(ViewQuizListByCategory, self).\
            dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ViewQuizListByCategory, self)\
            .get_context_data(**kwargs)

        context['category'] = self.category
        return context

    def get_queryset(self):
        queryset = super(ViewQuizListByCategory, self).get_queryset()
        return queryset.filter(category=self.category, draft=False)


class QuizUserProgressView(TemplateView):
    template_name = 'progress.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(QuizUserProgressView, self)\
            .dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(QuizUserProgressView, self).get_context_data(**kwargs)
        progress, c = Progress.objects.get_or_create(user=self.request.user)
        context['cat_scores'] = progress.list_all_cat_scores
        context['exams'] = progress.show_exams()
        return context


class QuizMarkingList(QuizMarkerMixin, SittingFilterTitleMixin, ListView):
    model = Sitting

    def get_queryset(self):
        queryset = super(QuizMarkingList, self).get_queryset()\
                                               .filter(complete=True)

        user_filter = self.request.GET.get('user_filter')
        if user_filter:
            queryset = queryset.filter(user__username__icontains=user_filter)

        return queryset


class QuizMarkingDetail(QuizMarkerMixin, DetailView):
    model = Sitting

    def post(self, request, *args, **kwargs):
        sitting = self.get_object()

        q_to_toggle = request.POST.get('qid', None)
        if q_to_toggle:
            q = Question.objects.get_subclass(id=int(q_to_toggle))
            if int(q_to_toggle) in sitting.get_incorrect_questions:
                sitting.remove_incorrect_question(q)
            else:
                sitting.add_incorrect_question(q)

        return self.get(request)

    def get_context_data(self, **kwargs):
        context = super(QuizMarkingDetail, self).get_context_data(**kwargs)
        context['questions'] =\
            context['sitting'].get_questions(with_answers=True)
        return context


class QuizTake(FormView):
    form_class = QuestionForm
    template_name = 'question.html'
    result_template_name = 'result.html'
    single_complete_template_name = 'single_complete.html'

    def dispatch(self, request, *args, **kwargs):
        self.quiz = get_object_or_404(Quiz, url=self.kwargs['quiz_name'])
        if self.quiz.draft and not request.user.has_perm('quiz.change_quiz'):
            raise PermissionDenied

        try:
            self.logged_in_user = self.request.user.is_authenticated()
        except TypeError:
            self.logged_in_user = self.request.user.is_authenticated

        if self.logged_in_user:
            self.sitting = Sitting.objects.user_sitting(request.user,
                                                        self.quiz)
        else:
            self.sitting = self.anon_load_sitting()

        if self.sitting is False:
            return render(request, self.single_complete_template_name)

        return super(QuizTake, self).dispatch(request, *args, **kwargs)

    def get_form(self, *args, **kwargs):
        if self.logged_in_user:
            self.question = self.sitting.get_first_question()
            self.progress = self.sitting.progress()
        else:
            self.question = self.anon_next_question()
            self.progress = self.anon_sitting_progress()

        if self.question.__class__ is Essay_Question:
            form_class = EssayForm
        else:
            form_class = self.form_class

        return form_class(**self.get_form_kwargs())

    def get_form_kwargs(self):
        kwargs = super(QuizTake, self).get_form_kwargs()

        return dict(kwargs, question=self.question)

    def form_valid(self, form):
        if self.logged_in_user:
            self.form_valid_user(form)
            if self.sitting.get_first_question() is False:
                return self.final_result_user()
        else:
            self.form_valid_anon(form)
            if not self.request.session[self.quiz.anon_q_list()]:
                return self.final_result_anon()

        self.request.POST = {}

        return super(QuizTake, self).get(self, self.request)

    def get_context_data(self, **kwargs):
        context = super(QuizTake, self).get_context_data(**kwargs)
        context['question'] = self.question
        context['quiz'] = self.quiz
        if hasattr(self, 'previous'):
            context['previous'] = self.previous
        if hasattr(self, 'progress'):
            context['progress'] = self.progress
        return context

    def form_valid_user(self, form):
        progress, c = Progress.objects.get_or_create(user=self.request.user)
        guess = form.cleaned_data['answers']
        is_correct = self.question.check_if_correct(guess)

        if is_correct is True:
            self.sitting.add_to_score(1)
            progress.update_score(self.question, 1, 1)
        else:
            self.sitting.add_incorrect_question(self.question)
            progress.update_score(self.question, 0, 1)

        if self.quiz.answers_at_end is not True:
            self.previous = {'previous_answer': guess,
                             'previous_outcome': is_correct,
                             'previous_question': self.question,
                             'answers': self.question.get_answers(),
                             'question_type': {self.question
                                               .__class__.__name__: True}}
        else:
            self.previous = {}

        self.sitting.add_user_answer(self.question, guess)
        self.sitting.remove_first_question()

    def final_result_user(self):
        results = {
            'quiz': self.quiz,
            'score': self.sitting.get_current_score,
            'max_score': self.sitting.get_max_score,
            'percent': self.sitting.get_percent_correct,
            'sitting': self.sitting,
            'previous': self.previous,
        }

        self.sitting.mark_quiz_complete()

        if self.quiz.answers_at_end:
            results['questions'] =\
                self.sitting.get_questions(with_answers=True)
            results['incorrect_questions'] =\
                self.sitting.get_incorrect_questions

        if self.quiz.exam_paper is False:
            self.sitting.delete()

        return render(self.request, self.result_template_name, results)

    def anon_load_sitting(self):
        if self.quiz.single_attempt is True:
            return False

        if self.quiz.anon_q_list() in self.request.session:
            return self.request.session[self.quiz.anon_q_list()]
        else:
            return self.new_anon_quiz_session()

    def new_anon_quiz_session(self):
        """
        Sets the session variables when starting a quiz for the first time
        as a non signed-in user
        """
        self.request.session.set_expiry(259200)  # expires after 3 days
        questions = self.quiz.get_questions()
        question_list = [question.id for question in questions]

        if self.quiz.random_order is True:
            random.shuffle(question_list)

        if self.quiz.max_questions and (self.quiz.max_questions
                                        < len(question_list)):
            question_list = question_list[:self.quiz.max_questions]

        # session score for anon users
        self.request.session[self.quiz.anon_score_id()] = 0

        # session list of questions
        self.request.session[self.quiz.anon_q_list()] = question_list

        # session list of question order and incorrect questions
        self.request.session[self.quiz.anon_q_data()] = dict(
            incorrect_questions=[],
            order=question_list,
        )

        return self.request.session[self.quiz.anon_q_list()]

    def anon_next_question(self):
        next_question_id = self.request.session[self.quiz.anon_q_list()][0]
        return Question.objects.get_subclass(id=next_question_id)

    def anon_sitting_progress(self):
        total = len(self.request.session[self.quiz.anon_q_data()]['order'])
        answered = total - len(self.request.session[self.quiz.anon_q_list()])
        return (answered, total)

    def form_valid_anon(self, form):
        guess = form.cleaned_data['answers']
        is_correct = self.question.check_if_correct(guess)

        if is_correct:
            self.request.session[self.quiz.anon_score_id()] += 1
            anon_session_score(self.request.session, 1, 1)
        else:
            anon_session_score(self.request.session, 0, 1)
            self.request\
                .session[self.quiz.anon_q_data()]['incorrect_questions']\
                .append(self.question.id)

        self.previous = {}
        if self.quiz.answers_at_end is not True:
            self.previous = {'previous_answer': guess,
                             'previous_outcome': is_correct,
                             'previous_question': self.question,
                             'answers': self.question.get_answers(),
                             'question_type': {self.question
                                               .__class__.__name__: True}}

        self.request.session[self.quiz.anon_q_list()] =\
            self.request.session[self.quiz.anon_q_list()][1:]

    def final_result_anon(self):
        score = self.request.session[self.quiz.anon_score_id()]
        q_order = self.request.session[self.quiz.anon_q_data()]['order']
        max_score = len(q_order)
        percent = int(round((float(score) / max_score) * 100))
        session, session_possible = anon_session_score(self.request.session)
        if score is 0:
            score = "0"

        results = {
            'score': score,
            'max_score': max_score,
            'percent': percent,
            'session': session,
            'possible': session_possible
        }

        del self.request.session[self.quiz.anon_q_list()]

        if self.quiz.answers_at_end:
            results['questions'] = sorted(
                self.quiz.question_set.filter(id__in=q_order)
                                      .select_subclasses(),
                key=lambda q: q_order.index(q.id))

            results['incorrect_questions'] = (
                self.request
                    .session[self.quiz.anon_q_data()]['incorrect_questions'])

        else:
            results['previous'] = self.previous

        del self.request.session[self.quiz.anon_q_data()]

        return render(self.request, 'result.html', results)


def anon_session_score(session, to_add=0, possible=0):
    """
    Returns the session score for non-signed in users.
    If number passed in then add this to the running total and
    return session score.

    examples:
        anon_session_score(1, 1) will add 1 out of a possible 1
        anon_session_score(0, 2) will add 0 out of a possible 2
        x, y = anon_session_score() will return the session score
                                    without modification

    Left this as an individual function for unit testing
    """
    if "session_score" not in session:
        session["session_score"], session["session_score_possible"] = 0, 0

    if possible > 0:
        session["session_score"] += to_add
        session["session_score_possible"] += possible

    return session["session_score"], session["session_score_possible"]




def add_mc_answer(request):
    # myform = MCAnswerForm()
    myform = QuestionFormSet()
    course = request.user.courses_joined.all().first()
    quiz = Quiz.objects.get(course = course)
    question_data = request.POST.get("question")
    content = request.POST
  
    context = {
        'formset':myform
    }
    
    print("request data ",request.POST)

    if request.method == "POST":
        myform = QuestionFormSet(request.POST or None)
        question = MCQuestion.objects.create(answer_order = "random",figure = "",content = question_data)
        question.quiz.add(quiz)
       
        
        if myform.is_valid():
            print("form is ",myform.data)
            return HttpResponse("Created")
    
        return render(request,"instructor/quiz/mc_answer.html",context)
    

    return render(request,"instructor/quiz/mc_answer.html",context)



