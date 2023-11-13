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
    sort_by = request.GET.get('sort_by') if request.GET.get('sort_by') is not None else '-created_at'
    if sort_by in ['views', 'votes']:
        questions = Question.objects.annotate(total=Count(sort_by)).order_by('-total')
    else:
        questions = Question.objects.all().order_by(sort_by)
    return render(request, 'QandA.html', {'tag_categories':tag_categories,'questions':questions ,'sort':sort_by})

def get_tags(request):
    category_id = request.GET.get('category_id')
    # Retrieve tags based on the selected category
    if category_id:
        tags = Tag.objects.filter(category=category_id).values('id', 'name')
    else:
        # If no category is selected, return all tags
        tags = Tag.objects.values('id', 'name')
    # Convert the queryset to a list of dictionaries
    tags_list = list(tags)
    # Return a JSON response
    return JsonResponse({'tags': tags_list})