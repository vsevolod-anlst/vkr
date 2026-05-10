import os
import requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

def send_telegram_message(chat_id: int, text: str): # наверное лучше чтобы он клеил вопрос с ответом?
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    r = requests.post(url, json={"chat_id": chat_id, "text": text})
    if r.status_code == 429:
        raise Exception("Rate limit")
