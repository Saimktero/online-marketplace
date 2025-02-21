from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Указываем Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketplace.settings')

celery_app = Celery('marketplace')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')

# Добавляем настройку для устранения предупреждения
celery_app.conf.broker_connection_retry_on_startup = True

celery_app.autodiscover_tasks()


@celery_app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')