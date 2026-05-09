# backend/app/celery_app.py

from celery import Celery

celery_app = Celery(
    "rag",
    broker="amqp://guest:guest@rag-rabbitmq:5672//",
    backend="rpc://"
)

celery_app.autodiscover_tasks(["app"])
