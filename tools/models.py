from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()


class PromptLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    prompt = models.TextField() 
    response = models.TextField(null=True, blank=True) 
    status = models.CharField(max_length=10, null=True, blank=True) 
    timestamp = models.DateTimeField(auto_now_add=True)  
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    model = models.CharField(max_length=24)
    image = models.ImageField(upload_to='prompt_images/', null=True, blank=True)
    tokens = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Prompt by {self.user.username if self.user else 'Anonymous'} at {self.timestamp}"