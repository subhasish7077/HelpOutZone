from django.urls import path
from .views import *

app_name = 'authuser'

urlpatterns = [
    path('login/',login_register,name='login'),
    path('logout/',logout_page,name='logout'),
    path('user/profile/<pk>', user_profile, name='user_profile'),
    path('user/update/user', updateUserChanges, name='userUpdate'),
    path('user/change/password', change_password, name='change_password'),
]