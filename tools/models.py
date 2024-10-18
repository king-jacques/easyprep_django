from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now
# from .utils import generate_api_key
# Create your models here.

User = get_user_model()

def generate_key():
    from .utils import generate_api_key
    return generate_api_key()

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

class APIKey(models.Model):
    key = models.CharField(max_length=50, unique=True, default=generate_key)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    last_used = models.DateTimeField(null=True, blank=True)  # Track last used time
    usage_count = models.PositiveIntegerField(default=0)
    request_rate = models.PositiveIntegerField(default=60) 

    def __str__(self):
        return self.key
    
    @staticmethod
    def generate_key():
        from tools.utils import generate_api_key
        return generate_api_key()  # Generates a secure random API key


    def increment_usage(self):
        self.usage_count += 1
        self.last_used = now()
        self.save()

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        super().save(*args, **kwargs)