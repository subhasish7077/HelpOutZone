from django.urls import path
from . import views
app_name = 'QandA'
urlpatterns = [
    path('sp/<pk>',views.try_temp,name='try'),
    path('QandA/',views.QandA_temp,name='QandA'),
]