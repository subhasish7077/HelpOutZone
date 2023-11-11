from django.urls import path
from . import views
app_name = 'QandA'
urlpatterns = [
    path('QandA/<pk>',views.get_questionByID,name='Question_byid'),
    path('QandA/',views.Questionsview,name='questions_list'),
]