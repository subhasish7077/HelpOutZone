from django import forms
from django.contrib.auth import authenticate, login
from .models import *

class UserForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control'}))
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'app_password', 'openai_api_key', 'password')
        widgets = {
            'first_name' : forms.TextInput(attrs={'class' : 'form-control'}),
            'last_name' : forms.TextInput(attrs={'class' : 'form-control'}),
            'username' : forms.TextInput(attrs={'class' : 'form-control'}),
            'email' : forms.EmailInput(attrs={'class' : 'form-control'}),
            'password' : forms.PasswordInput(attrs={'class' : 'form-control'}),
            'app_password':forms.PasswordInput(attrs={'class':'form-control'}),
            'openai_api_key' : forms.TextInput(attrs={'class' : 'form-control'}),
            }

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        open_api_key = cleaned_data.get('openai_api_key')

        if password != confirm_password:
            raise forms.ValidationError("password and confirm_password does not match")
        if open_api_key is None or len(open_api_key) != 51 or open_api_key[:3]!='sk-':
            raise forms.ValidationError("Enter valid openai api key")
