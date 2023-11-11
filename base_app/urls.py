from django.urls import path
from . import views
app_name = 'base_app'
urlpatterns = [
    path('',views.home,name='home page'),
    path('/about',views.about,name='about'),
    
]