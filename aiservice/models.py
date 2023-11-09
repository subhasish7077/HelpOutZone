from django.db import models
from authuser.models import User
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class emailGenerationDB(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='email_generation')
    prompt = models.TextField('prompt')
    subject = models.CharField('subject', max_length=255, blank=True, null=False)
    body = RichTextUploadingField()
    generated_at = models.DateTimeField(auto_now_add=True)
    token_used = models.IntegerField('Token used',default=0)
    def __str__(self):
        return self.prompt
    
class emailSent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_sent')
    subject = models.CharField('subject', max_length=255, blank=True, null=False)
    to = models.EmailField("to", max_length=254,null=False, blank=False)
    cc = models.TextField("CC", blank=True, null=True)
    body = RichTextUploadingField()
    sent_at = models.DateTimeField(auto_now_add=True)

class contentGenerationDB(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='content_generation')
    prompt = models.TextField('prompt')
    generated_content = models.TextField()
    generated_at = models.DateTimeField(auto_now_add=True)
    token_used = models.IntegerField('Token used',default=0)
    
    class Meta:
        ordering = ['generated_at']
    def __str__(self):
        return self.prompt