from django.db import models
from authuser.models import User
from datetime import datetime, timedelta
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class TagCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(TagCategory, on_delete=models.CASCADE, related_name="tags")
    
    class Meta:
        ordering=['category']
    
    def __str__(self):
        return self.name

class Question(models.Model):
    title = models.CharField(max_length=1000)
    description = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authors_questions')
    tags = models.ManyToManyField(Tag, related_name='question_tags')
    created_at = models.DateTimeField(auto_now_add=True)
    views = models.ManyToManyField(User, related_name='viewed',blank=True)
    total_votes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title

    def created_ago(self):
        now = timezone.now()
        delta = now - self.created_at
        year = delta.days // 365
        month = (delta.days % 365) // 30
        days = delta.days % 30
        hours, remainder = divmod(delta.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        
        time = ""
        if year > 0:
            time += f"{year} {'year' if year == 1 else 'years'} "
        if month > 0:
            time += f"{month} {'month' if month == 1 else 'months'} "
        if year == 0 and month == 0 and days > 0:
            time += f"{days} {'day' if days == 1 else 'days'}"
        elif days == 0:
            if hours > 0:
                time += f"{hours} {'hour' if hours == 1 else 'hours'}"
            if minutes > 0:
                time += f" {minutes} {'minute' if minutes == 1 else 'minutes'}"
            if hours == 0 and minutes < 3:
                return "just now"
            
        time += ' ago'
        return time
    
class Answer(models.Model):
    content = RichTextUploadingField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='authors_answer')
    created_at = models.DateTimeField(auto_now_add=True)
    total_votes = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Answer to {self.question.title}"

class Votes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authors_vote')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True, blank=True)
    vote_type = models.IntegerField(choices=((1, 'Upvote'), (-1, 'Downvote')))
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user','question','answer')