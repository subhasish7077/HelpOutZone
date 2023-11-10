from django.shortcuts import render
from django.views.generic import ListView, UpdateView, FormView
from .models import *
# Create your views here.
def try_temp(request,pk):
    print(pk)
    question = Question.objects.filter(id=pk)
    question = question[0]
    ans = question.answers.all()
    print(question.tags)
    return render(request, 'try.html',{'answers':ans,'question':question})

def QandA_temp(request):
    l = list(TagCategory.objects.all())
    l.sort(key=lambda x:x.name)
    questions = Question.objects.all()
    return render(request, 'QandA.html', {'l':l,'questions':questions})