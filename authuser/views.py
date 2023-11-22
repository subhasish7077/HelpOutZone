from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import User
from .forms import UserForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import update_session_auth_hash
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
def user_profile(request,pk):
    user = User.objects.filter(id=pk).first()
    if user == request.user:
        editable = request.session.get('editable',False)
    else:
        editable = False
    asked_questions = user.authors_questions.all()
    given_answer = user.authors_answer.all()
    return render(request, 'user_profile.html',{'user':user,'editable':editable,'asked_questions':asked_questions,'given_answers':given_answer})

@login_required(login_url='authuser:login')
def updateUserChanges(request):
    user=get_object_or_404(User,id=request.user.id)
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name',user.first_name)
        user.last_name = request.POST.get('last_name',user.last_name)
        user.username = request.POST.get('username',user.username)
        user.app_password = request.POST.get('app_password',user.app_password)
        user.openai_api_key = request.POST.get('openai_api_key',user.openai_api_key)
        user.bio = request.POST.get('bio',user.bio)
        user.save()
        request.session['editable'] = False
    else:
        request.session['editable'] = True
    return redirect('authuser:user_profile',pk=user.id)

@login_required(login_url='authuser:login')
def change_password(request):
    print('spsps')
    if request.method == 'POST':
        print('request')
        old_password = request.POST.get('old_password')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        print(old_password, password1, password2)
        if request.user.check_password(old_password):
            print('old password')
            
            if password1 == password2:
                request.user.set_password(password1)
                request.user.save()
                print('saved')
                
                update_session_auth_hash(request, request.user)
                messages.success(request,"Password changes Successfully")
            else:
                messages.error(request,"Password does not match")
        else:
            messages.error(request,'Old password is Incorrect')
    else:
        messages.error(request,"Error Occurred")
    print(request.POST)
    return redirect('authuser:user_profile',pk=request.user.id)