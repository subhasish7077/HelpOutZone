from django.shortcuts import render
from QandA.models import TagCategory, Question

# Create your views here.
def home(request):
    return render(request, 'home.html')

def try_temp(request):
    return render(request, 'try.html')

def QandA_temp(request):
    l = list(TagCategory.objects.all())
    l.sort(key=lambda x:x.name)
    questions = Question.objects.all()
    questions = [questions[1] for i in range(10)]
    return render(request, 'QandA.html', {'l':l,'questions':questions})