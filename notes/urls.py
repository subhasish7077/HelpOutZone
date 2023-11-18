# urls.py
from django.urls import path
from .views import file_upload, file_list, search_posts,download_file
app_name='notes'
urlpatterns = [
    path('upload/', file_upload, name='file_upload'),
    path('files/', file_list, name='file_list'),
    path('download/<int:file_id>/', download_file, name='download_file'),
    path('search/', search_posts, name='search_posts'),

]