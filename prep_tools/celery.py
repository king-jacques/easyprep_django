import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'prep_tools.settings')

celery_app = Celery('prep_tools')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()

# celery -A prep_tools worker -E -l info
# wrap tasks with @shared_tasks