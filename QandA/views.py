from turtle import title
from django.shortcuts import redirect, render
from django.db.models.functions import Length
from django.db.models import Count
from django.urls import reverse
from .models import *
from django.http import JsonResponse, HttpResponseRedirect
# Create your views here.

def get_questionByID(request,pk):
    question = Question.objects.filter(id=pk)[0]
    def update_views(question):
        if question.views.filter(id = request.user.id).exists():
            pass
        else:
            question.views.add(request.user.id)
    update_views(question)        
    answers = question.answers.all()
    return render(request, 'try.html',{'answers':answers,'question':question})

def Questionsview(request):
    tag_categories = list(TagCategory.objects.all())
    tag_categories.sort(key=lambda x:x.name)
    questions = Question.objects.all()
    search_text = request.GET.get('question_search') or ""
    if search_text:
        questions = questions.filter(title__icontains=search_text)
    tags = request.GET.getlist('tags')
    sort_by = request.GET.get('sort_by') or '-created_at'
    if tags:
        questions = questions.filter(tags__id__in=tags).distinct()
    if sort_by in ['views', 'votes']:
        questions = questions.annotate(total=Count(sort_by)).order_by('-total')
    else:
        questions=questions.order_by(sort_by)
    return render(request, 'QandA.html', {'tag_categories':tag_categories,'questions':questions ,'sort':sort_by,'search':search_text})

def get_tags(request):
    category_id = request.GET.get('category_id')
    if category_id:
        tags = Tag.objects.filter(category=category_id).values('id', 'name')
    else:
        tags = Tag.objects.values('id', 'name')
    tags_list = list(tags)
    return JsonResponse({'tags': tags_list})