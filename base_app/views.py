from django.shortcuts import render
from QandA.models import TagCategory, Question, Answer

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')