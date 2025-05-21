from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

#app.conf.beat_schedule = {
 #   'check-inactive-users-every-day': {
  #      'task' : 'config.tasks.check_inactive_users',
   #     'schedule': crontab(hour=3, minute=0),
    #},
#}

app.autodiscover_tasks()