from django.urls import path
from django.contrib.auth import views as auth_view
from .views import *

app_name = 'authuser'

urlpatterns = [
    path('login/',login_register,name='login'),
    path('logout/',logout_page,name='logout'),
]