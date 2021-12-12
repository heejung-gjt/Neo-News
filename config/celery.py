from __future__ import absolute_import, unicode_literals

from celery import Celery
from celery.schedules import crontab

import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('config', broker='amqp://', backend='rpc://', include=['user.tasks'])
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

app.conf.beat_schedule = {
    'add-every-minutes-naver':{
    'task':'user.tasks.task_scrappy_naver',
    'schedule': crontab(minute='*/3'),
    },
    'add-every-minutes-daum':{
    'task':'user.tasks.task_scrappy_daum',
    'schedule': crontab(minute='*/5'),
    }
}
