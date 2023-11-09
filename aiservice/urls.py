from django.urls import path
from .views import *

app_name = 'aiservice'

urlpatterns = [
    path('email/handle/', handle_email,name='send_email'),
    path('content/generator/', content_generation,name='content_generator'),
    path('content/by/<id>',get_content_byID,name='contentbyid'),
    path('email/by/<id>',get_email_byID,name='emailbyid'),
]