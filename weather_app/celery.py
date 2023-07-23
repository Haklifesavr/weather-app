# celery.py

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather.settings')

app = Celery('weather_app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# weather_app/celery.py

# from celery import Celery
# from django.conf import settings

# app = Celery('weather_app')
# app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)