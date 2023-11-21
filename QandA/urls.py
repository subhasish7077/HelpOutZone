from django.urls import path
from . import views
app_name = 'QandA'
urlpatterns = [
    path('QandA/<pk>',views.get_questionByID,name='Question_byid'),
    path('QandA/',views.Questionsview,name='questions_list'),
    path('get_tags/', views.get_tags, name='get_tags'),
    path('QandA/tag/<pk>/', views.QuestionsByTags, name='get_question_by_tags'),
    path('QandA/answer/delete/', views.deleteanswer, name='delete_answer'),
    path('QandA/update/answer/<pk>/', views.updateAnswer, name='update_answer'),
    path('QandA/save/changed/answer/<pk>/',views.saveChangedAnswer, name='save_changes'),
    path('QandA/Upvote/question/<pk>', views.Upvote_question, name='UpvoteQuestion'),
    path('QandA/Downvote/question/<pk>', views.Downvote_question, name='DownvoteQuestion'),
    path('QandA/Upvote/answer/<pk>', views.Upvote_answer, name='UpvoteAnswer'),
    path('QandA/Downvote/answer/<pk>', views.Downvote_answer, name='DownvoteAnswer'),
]
