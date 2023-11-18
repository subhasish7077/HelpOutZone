from django.urls import path
from . import views
app_name = 'QandA'
urlpatterns = [
    path('QandA/<pk>',views.get_questionByID,name='Question_byid'),
    path('QandA/',views.Questionsview,name='questions_list'),
    path('get_tags/', views.get_tags, name='get_tags'),
    path('QandA/tag/<pk>/', views.QuestionsByTags, name='get_question_by_tags'),
    path('QandA/answer/delete/', views.deleteanswer, name='delete_answer'),
]
