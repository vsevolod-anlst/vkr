from app.celery_app import celery_app
from app.telegram import send_telegram_message
import time
import threading

lock = threading.Lock()

MIN_DELAY_GLOBAL = 0.05 # ограничение ТГ 30 сообщений в секунду, потому тут будет 20 максимум
MIN_DELAY_PER_CHAT = 1.0 # 1 сообще в сек в 1 чат
last_sent_global = 0.0
last_sent_per_chat = {}

@celery_app.task(queue="send_message", max_retries=5)
def send_message(chat_id: int, text: str, message_id: int):
    global last_sent_global, last_sent_per_chat

    with lock:
        now = time.time()

        delta_global = now - last_sent_global
        if delta_global < MIN_DELAY_GLOBAL:
            time.sleep(MIN_DELAY_GLOBAL - delta_global)

        last_chat_time = last_sent_per_chat.get(chat_id, 0)
        delta_chat = now - last_chat_time
        if delta_chat < MIN_DELAY_PER_CHAT:
            time.sleep(MIN_DELAY_PER_CHAT - delta_chat)

        try:
            send_telegram_message(chat_id, text, message_id)
        except Exception as e:
            raise send_message.retry(exc=e, countdown=1)

        last_sent_global = time.time()
        last_sent_per_chat[chat_id] = last_sent_global
