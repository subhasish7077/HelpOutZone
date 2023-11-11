from django.db import models
from authuser.models import User
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
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    tags = models.ManyToManyField(Tag, related_name='question_tags')
    created_at = models.DateTimeField(auto_now_add=True)
    votes = models.ManyToManyField(User, related_name='Ques_votes',blank=True)
    views = models.ManyToManyField(User, related_name='viewed',blank=True)

    def __str__(self):
        return self.title

class Answer(models.Model):
    content = RichTextUploadingField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    votes = models.ManyToManyField(User, related_name='ans_votes',blank=True)

    def __str__(self):
        return f"Answer to {self.question.title}"