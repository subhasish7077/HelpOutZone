from django.urls import path
from . import views
app_name = 'QandA'
urlpatterns = [
    path('tags/',views.QuestionUpdateView.as_view(),name='tags'),
]