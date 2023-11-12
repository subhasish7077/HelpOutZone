from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from .forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.

def login_register(request):
    form = UserForm()
    if request.method == 'POST':
        # for login form
        if request.POST.get('login button') == 'login':
            data = request.POST   
            email = data.get('email')
            password = data.get('password')
            if not User.objects.filter(email = email).exists():
                messages.error(request, 'User does not exits. Register your self')
                return redirect('authuser:login')
            else:
                user = authenticate(email=email, password=password)
                if user is None:
                    messages.error(request, 'Invalid Credentials Try Email and Password does not match')
                    return redirect('authuser:login')
                else:
                    login(request, user)
                    messages.success(request , 'login successful')
                    return redirect('base_app:home page')
        elif request.POST.get('register button') == 'register':
            # for register form
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
                # if successfully registered than login the user and redirect to home page
                user = authenticate(email=email, password=password)
                login(request, user)
                messages.success(request, "registration success")
                return redirect('base_app:home page')
            else:
                messages.error(request, form.errors)
                return redirect('authuser:login')
    return render(request,"login.html",{'form':form})

def logout_page(request):
    logout(request)
    messages.success(request, "successfully logged out")
    return redirect('base_app:home page')