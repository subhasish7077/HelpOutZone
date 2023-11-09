from django.contrib import admin
from .models import emailGenerationDB, emailSent, contentGenerationDB
# Register your models here.
admin.site.register(emailGenerationDB)
admin.site.register(emailSent)
admin.site.register(contentGenerationDB)