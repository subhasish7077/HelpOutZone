from django.db import models
from authuser.models import User

class FileUpload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    upload_date = models.DateTimeField(auto_now_add=True)
    tags = models.CharField(max_length=255)  # Assuming tags are stored as a comma-separated string

    def __str__(self):
        return self.file.name
