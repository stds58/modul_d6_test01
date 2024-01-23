import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test01.settings')

app = Celery('test01')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()