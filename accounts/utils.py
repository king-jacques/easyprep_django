from .models import ActivityLog
import json

def log_activity(request, action='default',**kwargs):

    user = kwargs.get('user', request.user)
    referrer = request.META.get('HTTP_REFERER', None)
    user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
    ip_address = request.META.get('REMOTE_ADDR')
    url = request.build_absolute_uri(),
    resource_type = kwargs.get('resource_type')
    resource_id = kwargs.get('resource_id')
    status = kwargs.get('status', 'default')
    info = kwargs.get('info', {})
    type = kwargs.get('type', 'logging')
    extra_info = {
        'url': str(url),
    }
    extra_info |= info

    try:
        info = json.dumps(extra_info)
    except Exception as e:
        info = str(url) + str(e) 
    try:
       ActivityLog.objects.create(
           user=user,
           action=action,
           ip_address=ip_address,
           referrer = referrer,
           user_agent = user_agent,
           resource_id = resource_id,
           resource_type = resource_type,
           status = status,
           info = info,
           type = type

       )
    except Exception as e:
        ActivityLog.objects.create(
            action='exception',
            status = 'exception',
            ip_address=ip_address,
            referrer = referrer,
            user_agent = user_agent,
            info = str(e),
            type = 'critical'
        )
     