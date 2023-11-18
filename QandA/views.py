from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.html import strip_tags
from django.db.models import Count
from django.contrib import messages
from django.urls import reverse
from .models import *
from .forms import *
import re

# Create your views here.

def add_answer(request, question):
    form = AnswerForm(request.POST)
    if form.is_valid():
        content = form.cleaned_data.get('content', '')
        temp_content = re.sub(r'&nbsp;|&#160;', ' ', content)
        if strip_tags(temp_content).strip():
            try:
                Answer.objects.create(
                    content=content,
                    question=question,
                    author=request.user
                )
                messages.success(request, "Answer submitted successfully")
            except Exception as e:
                messages.error(request, f"Error saving answer: {e}")
        else:
            messages.error(request, "Content is empty")

def update_views(request, question):
    if not question.views.filter(id=request.user.id).exists():
        question.views.add(request.user.id)
        
@login_required(login_url='authuser:login')
def get_questionByID(request, pk):
    question = Question.objects.filter(id=pk).first()

    if request.method == 'POST':
        add_answer(request, question)
        return redirect('QandA:Question_byid', pk=pk)

    update_views(request, question)
    answers = question.answers.all()

    return render(request, 'Questiondetails.html', {'answers': answers, 'question': question, 'form': AnswerForm()})

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def filter_questions_by_search_text(questions, search_text):
    if search_text:
        return questions.filter(title__icontains=search_text)
    return questions

def filter_questions_by_tag_category(questions, tag_category_id):
    if tag_category_id:
        tag_category = TagCategory.objects.filter(id=tag_category_id).first()
        if tag_category:
            tags = tag_category.tags.all()
            return questions.filter(tags__in=tags).distinct()
    return questions

def filter_questions_by_selected_tags(questions, selected_tags):
    if selected_tags:
        return questions.filter(tags__in=selected_tags).distinct()
    return questions

def sort_questions(questions, sort_by):
    if sort_by in ['views', 'votes']:
        return questions.annotate(total=Count(sort_by)).order_by('-total')
    return questions.order_by(sort_by)

@login_required(login_url='authuser:login')
def Questionsview(request):
    tag_categories = TagCategory.objects.all().order_by('name')
    tag_id = request.session.pop('tag_id', None)
    questions = Tag.objects.filter(id=tag_id).first().question_tags.all() if tag_id else Question.objects.all()
    search_text = request.GET.get('question_search', '')
    questions = filter_questions_by_search_text(questions, search_text)
    tag_category_id = request.GET.get('tagcategory') or -1
    questions = filter_questions_by_tag_category(questions, tag_category_id)
    selected_tags = request.GET.getlist('tags')
    questions = filter_questions_by_selected_tags(questions, selected_tags)
    sort_by = request.GET.get('sort_by', '-created_at')
    questions = sort_questions(questions, sort_by)

    context = {
        'tag_categories': tag_categories,
        'questions': questions,
        'sort': sort_by,
        'search': search_text,
        'tagcategories': int(tag_category_id),
    }

    return render(request, 'QandA.html', context)

@login_required(login_url='authuser:login')
def QuestionsByTags(request,pk):
    request.session['tag_id'] = pk
    return redirect('QandA:questions_list')

def get_tags(request):
    category_id = request.GET.get('category_id')
    if category_id:
        tags = Tag.objects.filter(category=category_id).values('id', 'name')
    else:
        tags = Tag.objects.values('id', 'name')
    tags_list = list(tags)
    return JsonResponse({'tags': tags_list})

@login_required(login_url='authuser:login')
def deleteanswer(request):
    pk = request.GET.get('delete_button') or '-1'
    answer = Answer.objects.filter(id=pk).first()
    question_id = answer.question.id
    answer.delete()
    return redirect('QandA:Question_byid',pk=question_id)