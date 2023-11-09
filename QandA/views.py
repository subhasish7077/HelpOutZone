from django.shortcuts import render
from django.views.generic import ListView, UpdateView, FormView
from .models import *
# Create your views here.

class Tagview(ListView):
    model = TagCategory
    template_name = 'tagview.html'
    context_object_name = 'tags'  

    # def get_queryset(self):
    #     # Retrieve data from both models and combine them as needed
    #     model1_data = Tag.objects.all()
    #     model2_data = TagCategory.objects.all()
        
    #     # Combine the data into a single list or queryset
    #     combined_data = [list(model1_data),list(model2_data)]
        
    #     return combined_data


class QuestionUpdateView(FormView):
    model = Question
    template_name = "trying.html"
