# backend/app/celery_app.py

from celery import Celery
from kombu import Queue

celery_app = Celery(
    "rag",
    broker="amqp://guest:guest@rag-rabbitmq:5672//",
    backend="rpc://"
)

celery_app.conf.task_queues = (
    Queue("rag"),
    Queue("send_message"),
)

celery_app.autodiscover_tasks(["app"])
