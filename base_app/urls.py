from django.urls import path
from . import views
app_name = 'base_app'
urlpatterns = [
    path('',views.home,name='home page'),
    path('sp/',views.try_temp,name='try'),
    path('QandA/',views.QandA_temp,name='QandA'),
]