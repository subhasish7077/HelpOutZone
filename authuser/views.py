from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import User
from .forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
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


@login_required(login_url='authuser:login')
def user_profile(request):
    user = request.user
    editable = True
    return render(request, 'user_profile.html',{'user':user,'editable':editable})

@login_required(login_url='authuser:login')
def updateUserChanges(request):
    user=get_object_or_404(User,id=request.user.id)
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.username = request.POST.get('username')
        user.app_password = request.POST.get('app_password')
        user.openai_api_key = request.POST.get('openai_api_key')
        user.save()
    
    return redirect('authuser:user_profile')