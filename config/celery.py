from __future__ import absolute_import, unicode_literals
import os
from datetime import timedelta

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

CELERY_BEAT_SCHEDULE = {
    'task-name': {
        'task': 'config.tasks.my_task',
        'schedule': timedelta(minutes=10),
    },
}

app.autodiscover_tasks()