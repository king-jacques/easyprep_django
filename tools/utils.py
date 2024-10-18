from .models import PromptLog
from .serializers import PromptLogSerializer
import json
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
        