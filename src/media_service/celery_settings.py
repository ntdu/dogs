import os

from celery import Celery
from kombu import Exchange, Queue

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.media_service.settings")

app = Celery("media_service")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.task_queues = [
    Queue("tasks", Exchange("tasks"), routing_key="tasks", queue_arguments={"x-max-priority": 10}),
    Queue("dead_letter", routing_key="dead_letter"),
]

app.autodiscover_tasks()
