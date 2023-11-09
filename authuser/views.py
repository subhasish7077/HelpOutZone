from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from .forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.

def register(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            confirm_password = request.POST.get('confirm_password')
            app_password = form.cleaned_data.get('app_password')
            openai_api_key = form.cleaned_data.get('openai_api_key')
            print(username,first_name,last_name, email,password,confirm_password,app_password,openai_api_key)
            user = User.objects.create(
                username = username,
                first_name = first_name,
                last_name = last_name,
                email = email,
                app_password = app_password,
                openai_api_key =openai_api_key
            )            
            user.set_password(password)
            user.save()
            messages.success(request, "registration success")
            return redirect('base_app:home page')
        else:
            messages.error(request, form.errors)
            return redirect('authuser:register')
    return render(request, 'registration.html',{'form':form})

def login_page(request):
    if request.method == 'POST':
        data = request.POST   
        email = data.get('email')
        password = data.get('password')
        if not User.objects.filter(email = email).exists():
            messages.error(request, 'User does not exits. Register your self')
            return redirect('authuser:register')
        else:
            user = authenticate(email=email, password=password)
            if user is None:
                messages.error(request, 'Invalid Credentials Try Email and Password does not match')
                return redirect('authuser:login')
            else:
                login(request, user)
                messages.success(request , 'login successful')
                return redirect('base_app:home page')
    return render(request,"login.html")

def logout_page(request):
    logout(request)
    messages.success(request, "successfully logged out")
    return redirect('base_app:home page')