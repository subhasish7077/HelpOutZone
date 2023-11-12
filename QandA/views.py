from django.shortcuts import render
from django.views.generic import ListView, UpdateView, FormView
from .models import *
from django.http import JsonResponse
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