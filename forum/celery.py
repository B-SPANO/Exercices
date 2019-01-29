import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_traceability.settings')

app = Celery(
    'django_traceability',
    broker='amqp://guest:guest@localhost',
    #include=['django_traceability.forum.tasks']
    )
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(['forum'])


if __name__ == '__main__':
    app.start()
