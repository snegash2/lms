try:
    from django.conf.urls import url
except ImportError:
    from django.urls import re_path as url,path

from .views import QuizListView,InstructorUpdateContentEditView, CategoriesListView, \
    ViewQuizListByCategory, QuizUserProgressView, QuizMarkingList, \
    QuizMarkingDetail, QuizDetailView, QuizTake,InstructorQuizEditView,\
        InstructorQuestionEditView,InstructorAnswerEditView,add_mc_answer,\
            InstructorListEditView,InstructorDeleteView,InstructorListSearchView,\
                InstructorListDeleteView,InstructorUpdateEditView
    


urlpatterns = [

    url(r'^instructor/edit-quiz/$',
        view=InstructorQuizEditView.as_view(),
        name='edit-quiz'),
    
    
    
    path('instructor/edit-question/',
        view=InstructorQuestionEditView.as_view(),
        name='edit-question'),

    
    
    path('instructor/list-question/',
        view=InstructorListEditView.as_view(),
        name='list-question'),
    
    
    path('instructor/search-question/',
        view=InstructorListSearchView.as_view(),
        name='search-question'),
    
    
        
    path('instructor/delete-question/',
        view=InstructorListDeleteView,
        name='delete-question'),
    
    
    path('instructor/update-question-content/',
        view=InstructorUpdateContentEditView,
        name='update-question-content'),
    
    path('instructor/update-question/',
        view=InstructorUpdateEditView,
        name='update-question'),
    
    url(r'^instructor/edit-answer/$',
        view=InstructorAnswerEditView.as_view(),
        name='edit-answer'),

    url(r'^$',
        view=QuizListView.as_view(),
        name='quiz_index'),

    url(r'^category/$',
        view=CategoriesListView.as_view(),
        name='quiz_category_list_all'),

    url(r'^category/(?P<category_name>[\w|\W-]+)/$',
        view=ViewQuizListByCategory.as_view(),
        name='quiz_category_list_matching'),

    url(r'^progress/$',
        view=QuizUserProgressView.as_view(),
        name='quiz_progress'),

    url(r'^marking/$',
        view=QuizMarkingList.as_view(),
        name='quiz_marking'),

    url(r'^marking/(?P<pk>[\d.]+)/$',
        view=QuizMarkingDetail.as_view(),
        name='quiz_marking_detail'),

    #  passes variable 'quiz_name' to quiz_take view
    url(r'^(?P<slug>[\w-]+)/$',
        view=QuizDetailView.as_view(),
        name='quiz_start_page'),

    url(r'^(?P<quiz_name>[\w-]+)/take/$',
        view=QuizTake.as_view(),
        name='quiz_question'),
    
    url('add_mc_answer',
        view=add_mc_answer,
        name='mc_answer'),
    
    
        
  
]
