from django.shortcuts import redirect, render
from django.utils.html import strip_tags
from django.db.models import Count
from django.contrib import messages
from django.urls import reverse
from .models import *
from .forms import *
import re
from django.http import JsonResponse, HttpResponseRedirect
# Create your views here.
    
def get_questionByID(request,pk):
    question = Question.objects.filter(id=pk)[0]
    form = AnswerForm()

    def add_answer():
        if request.method == 'POST':
            form = AnswerForm(request.POST)
            content = ""
            message = ""
            if form.is_valid():
                content = form.cleaned_data.get('content')
                tempcontent = re.sub(r'&nbsp;|&#160;', ' ', content)
            if strip_tags(tempcontent).strip():
                try:
                    obj = Answer.objects.create(
                        content = content,
                        question = question,
                        author = request.user
                    )
                    obj.save()
                    message = "Answer submitted successfully"
                except Exception as e:
                    print(f"save {e}")
            else:
                message = "Content is empty"
            if message :
                messages.success(request,message)
    add_answer()
    
    def update_views(question):
        if question.views.filter(id = request.user.id).exists():
            pass
        else:
            question.views.add(request.user.id)
    update_views(question)        
    answers = question.answers.all()
    return render(request, 'Questiondetails.html',{'answers':answers,'question':question,'form':form})

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
