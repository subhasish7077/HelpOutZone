from django import forms
from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class AnswerForm(forms.ModelForm):
    content = forms.CharField(
        
        widget = CKEditorUploadingWidget(config_name = 'config2'),  # Assuming you're using CKEditorUploadingWidget
        initial = "",
    )
    class Meta:
        model = Answer
        fields = ("content",)

class AnswerUpdateForm(forms.ModelForm):
    Update_content = forms.CharField(
        
        widget = CKEditorUploadingWidget(config_name = 'config2'),  # Assuming you're using CKEditorUploadingWidget
        initial = "",
    )
    class Meta:
        model = Answer
        fields = ("Update_content",)

class QuestionForm(forms.ModelForm):
    description = forms.CharField(
        widget = CKEditorUploadingWidget(config_name = 'config2'),  # Assuming you're using CKEditorUploadingWidget
        initial = "",
        )
    class Meta:
        model = Question
        fields = ("description",)
