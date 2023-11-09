from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager

class User(AbstractUser):
    username = models.CharField(max_length=50,null=True, blank=True)
    email = models.EmailField('email address', unique=True, null=False, blank=False)
    app_password = models.CharField("email app password", max_length=50)
    openai_api_key = models.CharField('api_key',max_length=51,null=False,blank=False,unique=True)
    total_token_used = models.IntegerField('Token used',default=0)

    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        ordering = ['email']
        
    
        
    
