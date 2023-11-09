from django import forms
from .models import emailGenerationDB
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class emailgenerateForm(forms.ModelForm):
    body = forms.CharField(
        widget=CKEditorUploadingWidget(),  # Assuming you're using CKEditorUploadingWidget
        initial="",
    )
    class Meta:
        model = emailGenerationDB
        fields = ('body',)