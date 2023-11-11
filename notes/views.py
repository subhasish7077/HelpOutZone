from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UploadedFile
from .forms import FileUploadForm
from django.http import HttpResponse


def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_instance = form.save(commit=False)
            file_instance.user = request.user
            file_instance.save()
            return redirect('notes:file_list')
    else:
        form = FileUploadForm()
    return render(request, 'upload_file.html', {'form': form})


def file_list(request):
    files = UploadedFile.objects.filter(user=request.user)
    return render(request, 'file_list.html', {'files': files})


def download_file(request, file_id):
    file = UploadedFile.objects.get(pk=file_id)
    response = HttpResponse(file.file, content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename="{file.file.name}"'
    return response
