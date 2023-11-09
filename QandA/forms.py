from django import forms
from .models import *

class QuestionForm(forms.ModelForm):
    
    class Meta:
        model = Question
        fields = '__all__'
