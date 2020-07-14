import os
from celery import Celery

# Задаем переменную окружения, содержащую название файла настроек нашего проекта.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'easyprbot_market.settings')

app = Celery('easyprbot_market')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
