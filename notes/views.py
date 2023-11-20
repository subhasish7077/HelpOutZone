from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import FileUpload
from .forms import FileUploadForm
from django.http import HttpResponse
@login_required(login_url='authuser:login')
def download_file(request, file_id):
    file = UploadedFile.objects.get(pk=file_id)
    response = HttpResponse(file.file, content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename="{file.file.name}"'
    return response

@login_required(login_url='authuser:login')
def file_upload(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_upload = form.save(commit=False)
            file_upload.user = request.user
            file_upload.save()
            return redirect('file_list')
    else:
        form = FileUploadForm()
    return render(request, 'upload_file.html', {'form': form})

@login_required(login_url='authuser:login')
def file_list(request):
    files = FileUpload.objects.all()
    return render(request, 'file_list.html', {'files': files})

@login_required(login_url='authuser:login')
def search_posts(request):
    if 'tag' in request.GET:
        tag = request.GET['tag']
        files = FileUpload.objects.filter(tags__icontains=tag)
    else:
        files = FileUpload.objects.all()
    return render(request, 'file_list.html', {'files': files})
