from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import emailgenerateForm
from .models import *
import openai


# Create your views here.
def generate_content(prompt:str, api_key:str) -> list:
    openai.api_key = api_key
    response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=250,
            temperature=0
            )
    content = str(response['choices'][0]['text']) 
    token_used = response['usage']['total_tokens'] 
    return [token_used, content]

def process_email_content(content:str) -> list:
    content = content.removeprefix('\n\n')
    content = content.split('\n\n')
    subject = content[0].removeprefix('Subject: ')
    body = ['<p>'+ item +'</p>' for item in content[1:]]
    body = '\n\n'.join(body)
    # print(body)
    return [subject, body]

def save_generated_content_DB(*args):
    try:
        obj = contentGenerationDB.objects.create(
            user = args[0],
            prompt = args[1],
            generated_content = args[2],
            token_used = args[3]
        )    
        obj.save()
        update_token_used(args[0],args[3])
        print('content saved')
    except Exception as e:
        print(e)

def update_token_used(user, token_used):
    try:
        user.total_token_used = user.total_token_used + token_used
        user.save()
    except Exception as e:
        print(e)

def send_email(*args):...

def process_prompt(prompt:str, type:str='content')-> str:
    if type == 'email':
        return 'compost an email for '+ prompt +' within 200 tokens'
    else:
        return prompt + ' within 200 tokens'

def reverse_process_prompt(prompt:str, type:str='content')-> str:
    if type == 'email':
        prompt = prompt.removeprefix('compost an email for')
    prompt = prompt.removesuffix('within 200 tokens')
    return prompt

def save_generated_email_DB(*args):
    try:
        temp = str(args[1]).removeprefix('compost an email for')
        temp = str(temp).removesuffix('within 200 tokens')
        obj = emailGenerationDB.objects.create(
            user = args[0],
            prompt = temp,
            subject = args[2],
            body = args[3],
            token_used = args[4]
        )    
        obj.save()
        print("email obj saved")
        update_token_used(args[0],args[4])
    except Exception as e:
        print(f"save {e}")

@login_required(login_url='authuser:login')
def handle_email(request):
    body=subject=prompt=""
    
    if 'prompt' in request.session:
        prompt = request.session['prompt']
        del request.session['prompt']
    if 'body' in request.session:
        body = request.session['body']
        del request.session['body']
    if 'subject' in request.session:
        subject = request.session['subject']
        del request.session['subject']
    
    if request.method == 'POST':
        btn=request.POST.get('submit_btn')
        if btn == 'generate':
            try:
                user = request.user
                prompt = request.POST.get('prompt')
                if prompt != "" and prompt is not None:
                    prompt = process_prompt(prompt,'email')
                    token_used, generated_email = generate_content(prompt, user.openai_api_key)
                    prompt = reverse_process_prompt(prompt,'email')
                    subject, body = process_email_content(generated_email)
                    save_generated_email_DB(user, prompt, subject, body, token_used)
                    messages.success(request, "Generated successfully")
                else:
                    messages.error("prompt is empty")
            except Exception as e:
                messages.error(request, 'Error Occurred: check your openai api_key and billing')
                print(e)
        elif btn == 'send':
            to = request.POST.get('to')
            cc = request.POST.get('cc')
            subject = request.POST.get('subject')
            form = emailgenerateForm(request.POST)
            if form.is_valid():
                body = form.cleaned_data.get('body')
            try:
                send_email(to, cc, subject, body)
                messages.success(request, "Mail send successfully")
            except Exception as e:
                print(e)
                messages.error(request, "error occurred")     
    
    form = emailgenerateForm(initial={'body':body})
    # display email generator history using paginator
    all_email_generated = emailGenerationDB.objects.filter(user=request.user).order_by('-generated_at')
    paginator = Paginator(all_email_generated, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request,'emailtemp.html',{'form':form,'subject':subject,'prompt':prompt,'email_history':page_obj})

@login_required(login_url='authuser:login')
def content_generation(request):
    content=prompt=""
    
    if 'content' in request.session:
        content = request.session['content']
        del request.session['content']
    if 'prompt' in request.session:
        prompt = request.session['prompt']
        del request.session['prompt']
        
    if request.method == 'POST':
        try:
            user = request.user
            prompt = request.POST.get('prompt')
            print(f"sipu {prompt} len: {len(prompt)}")
            if prompt != "" or prompt is not None:
                prompt = process_prompt(prompt)
                token_used, generated_content = generate_content(prompt, user.openai_api_key)
                prompt = reverse_process_prompt(prompt)
                save_generated_content_DB(user, prompt, generated_content, token_used)
                content = generated_content
                messages.success(request, "Generated successfully")
        except Exception as e:
            print(e)
    # display content history using paginator
    all_contents = contentGenerationDB.objects.filter(user=request.user).order_by('-generated_at')
    paginator = Paginator(all_contents, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
                request,'contentGeneration.html',
                {
                    'generated_content':content,'prompt':prompt, 'content_history':page_obj
                }
                )

@login_required(login_url='authuser:login')
def get_content_byID(request,id):
    content = contentGenerationDB.objects.filter(id=id)
    request.session['content'] = content[0].generated_content
    request.session['prompt'] = content[0].prompt
    return redirect('aiservice:content_generator')

@login_required(login_url='authuser:login')
def get_email_byID(request,id):
    content = emailGenerationDB.objects.filter(id=id)
    request.session['prompt'] = content[0].prompt
    request.session['subject'] = content[0].subject
    request.session['body'] = content[0].body
    print(request.session['body'])
    return redirect('aiservice:send_email')