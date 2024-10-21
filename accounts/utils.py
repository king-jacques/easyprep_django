from .models import ActivityLog
import json
from functools import wraps
from django.urls import resolve
import logging
logger = logging.getLogger(__name__)

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
     


# Decorator factory that takes only kwargs
def log_view_activity(**kwargs):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **view_kwargs):
            url_name = resolve(request.path_info).url_name  
            log_activity(request.user, url_name or view_func.__name__, **kwargs)
            
            # Call the actual view function
            return view_func(request, *args, **view_kwargs)

        return wrapper
    return decorator




def log_view_activity(**kwargs):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **view_kwargs):
            url_name = resolve(request.path_info).url_name
            
            try:
                log_activity(request.user, url_name or request.path_info, **kwargs)
                response = view_func(request, *args, **view_kwargs)
                log_activity(request.user, url_name or request.path_info, status="success", **kwargs)
                return response
            
            except Exception as e:
                error_message = str(e)
                logger.error(f"Exception in view {view_func.__name__}: {error_message}", exc_info=True)
            
                log_activity(request.user, url_name or request.path_info, status="error", error_message=error_message, **kwargs)
                raise

        return wrapper
    return decorator