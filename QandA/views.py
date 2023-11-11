from django.shortcuts import render
from django.views.generic import ListView, UpdateView, FormView
from .models import *
# Create your views here.
def get_questionByID(request,pk):
    print(pk)
    question = Question.objects.filter(id=pk)
    question = question[0]
    answers = question.answers.all()

    return render(request, 'try.html',{'answers':answers,'question':question})

def Questionsview(request):
    tag_categories = list(TagCategory.objects.all())
    tag_categories.sort(key=lambda x:x.name)
    questions = Question.objects.all().order_by('-created_at')
    return render(request, 'QandA.html', {'tag_categories':tag_categories,'questions':questions})