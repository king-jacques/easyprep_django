from .models import APIKey, User, PromptLog
from .serializers import PromptLogSerializer
import json
import secrets
import string
from datetime import timedelta

def log_prompt(request, **kwargs):
    try:
        data = {
            "user": request.user.pk if request.user else None,
            "prompt": kwargs.get('prompt'),
            "response": kwargs.get('response'),
            "tokens": kwargs.get('tokens'),
            "ip_address": request.META.get('REMOTE_ADDR'),
            "image": request.FILES.get('image'),
            "model": kwargs.get('model'),
            "status": kwargs.get('status')
        }
        serializer = PromptLogSerializer(data = data)

        if serializer.is_valid():
            serializer.save()

        else:
            error = json.dumps(serializer.errors)
            PromptLog.objects.create(
                user = request.user,
                prompt = data.get('prompt') or error,
                response = error,
                status = 'invalid_serializer',
                model = data.get('model')

            )
    except Exception as e:
        PromptLog.objects.create(
            prompt=str(e),
            status='exception'
        )
        

def generate_api_key(length=40):
    characters = string.ascii_letters + string.digits  # Only letters and digits
    # Generate a secure random string
    api_key = ''.join(secrets.choice(characters) for i in range(length))
    # secrets.token_urlsafe(32)
    return api_key

def create_api_key_for_user(user):
    # Ensure the user object is valid
    
    if not isinstance(user, User):
        raise ValueError("Invalid user object")

    # Generate a new API key
    new_api_key = generate_api_key()

    # Create and save the APIKey object
    api_key_obj = APIKey.objects.create(user=user, key=new_api_key)

    # Return the new API key
    return api_key_obj


from django.utils import timezone
from rest_framework.response import Response
from rest_framework.exceptions import Throttled

def throttle_api_key(api_key: APIKey, minutes=1):
    now = timezone.now()
    time_threshold = now - timedelta(minutes=minutes)  # Check requests within the last minute
    
    if api_key.last_used and api_key.last_used > time_threshold:
        if api_key.usage_count >= api_key.request_rate:
            raise Throttled(detail="Request limit exceeded. Try again later.")
    api_key.increment_usage()