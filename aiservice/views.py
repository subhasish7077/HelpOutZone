from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import emailgenerateForm
from .models import *
import openai

def process_email_content(content):
    content = content.removeprefix('\n\n').split('\n\n')
    subject = content[0].removeprefix('Subject: ')
    body = '\n\n'.join(['<p>' + item + '</p>' for item in content[1:]])
    return subject, body

def save_generated_content_DB(user, prompt, generated_content, token_used):
    try:
        obj = contentGenerationDB.objects.create(
            user=user,
            prompt=prompt,
            generated_content=generated_content,
            token_used=token_used
        )
        obj.save()
        update_token_used(user, token_used)
        print('Content saved')
    except Exception as e:
        print(e)

def save_generated_email_DB(user, prompt, subject, body, token_used):
    try:
        obj = emailGenerationDB.objects.create(
            user=user,
            prompt=prompt,
            subject=subject,
            body=body,
            token_used=token_used
        )
        obj.save()
        update_token_used(user, token_used)
        print("Email object saved")
    except Exception as e:
        print(f"Save error: {e}")

def update_token_used(user, token_used):
    try:
        user.total_token_used += token_used
        user.save()
    except Exception as e:
        print(e)

def process_prompt(prompt: str, type: str = 'content'):
    return f'compost an email for {prompt} within 200 tokens' if type == 'email' else f'{prompt} within 200 tokens'

def reverse_process_prompt(prompt: str, type: str = 'content'):
    if type == 'email':
        prompt = prompt.removeprefix('compost an email for')
    return prompt.removesuffix('within 200 tokens')

def generate_content(prompt, api_key, prompt_type):
    openai.api_key = api_key
    prompt = process_prompt(prompt, prompt_type)
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=250,
        temperature=0
    )
    prompt = reverse_process_prompt(prompt, prompt_type)
    content = str(response['choices'][0]['text'])
    token_used = response['usage']['total_tokens']
    return token_used, content, prompt

def send_email(to, cc, subject, body):
    return True
# Views 

@login_required(login_url='authuser:login')
def handle_email(request):
    form = ""
    subject = request.session.get('subject', '')
    prompt = request.session.get('prompt', '')
    body =  request.session.get('body', '')

    if 'subject' in request.session:
        del request.session['subject']
    if 'body' in request.session:
        del request.session['body']
    if 'prompt' in request.session:
        del request.session['prompt']
    if request.method == 'POST':
        btn = request.POST.get('submit_btn')
        if btn == 'generate':
            try:
                user = request.user
                prompt = request.POST.get('prompt')
                if prompt!="" and prompt is not None:
                    token_used, generated_email, prompt = generate_content(prompt, user.openai_api_key, 'email')
                    subject, body = process_email_content(generated_email)
                    save_generated_email_DB(user, prompt, subject, body, token_used)
                    messages.success(request, "Generated successfully")
                else:
                    messages.error(request,"Prompt is empty")
            except Exception as e:
                messages.error(request, 'Error occurred: check your OpenAI API key and billing')
                print(e)
        elif btn == 'send':
            to = request.POST.get('to')
            cc = request.POST.get('cc')
            subject = request.POST.get('subject')
            # body = emailgenerateForm(request.POST).cleaned_data.get('body')
            try:
                send_email(to, cc, subject,'sp')
                messages.success(request, "Mail sent successfully")
            except Exception as e:
                print(e)
                messages.error(request, "Error occurred")
    
    form = emailgenerateForm(initial={'body': body})
    all_email_generated = emailGenerationDB.objects.filter(user=request.user).order_by('-generated_at')
    paginator = Paginator(all_email_generated, 13)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
        
    return render(request, 'emailtemp.html', {'form': form, 'email_history': page_obj,'prompt':prompt,'subject':subject})

@login_required(login_url='authuser:login')
def content_generation(request):
    prompt = request.session.get('prompt', '')
    generated_content = request.session.get('content', '')
    if 'content' in request.session:
        del request.session['content']
    if 'prompt' in request.session:
        del request.session['prompt']
        
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        if prompt!="" and prompt is not None:
            try:
                user = request.user
                token_used, generated_content, prompt = generate_content(prompt, user.openai_api_key, 'content')
                save_generated_content_DB(user, prompt, generated_content, token_used)
                messages.success(request, "Generated successfully")
            except Exception as e:
                messages.success(request, f"Error Ocurred: {e}")
                print(e)
        else:
            messages.error(request,'Prompt is empty')

    all_contents = contentGenerationDB.objects.filter(user=request.user).order_by('-generated_at')
    paginator = Paginator(all_contents, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
        
    return render(
        request, 'contentGeneration.html',
        {
            'content_history': page_obj,
            'generated_content':generated_content,
            'prompt':prompt
        }
    )

@login_required(login_url='authuser:login')
def get_content_byID(request, id):
    content = contentGenerationDB.objects.filter(id=id).first()
    if content:
        request.session['content'] = content.generated_content
        request.session['prompt'] = content.prompt
    return HttpResponseRedirect(reverse('aiservice:content_generator'))


@login_required(login_url='authuser:login')
def get_email_byID(request, id):
    content = emailGenerationDB.objects.filter(id=id).first()
    if content:
        request.session['prompt'] = content.prompt
        request.session['subject'] = content.subject
        request.session['body'] = content.body
    return HttpResponseRedirect(reverse('aiservice:send_email'))