import os
import requests

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

def send_telegram_message(chat_id: int, text: str, message_id: int):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    r = requests.post(url, json={
        "chat_id": chat_id,
        "text": text,
        "reply_to_message_id": message_id
    })
    if r.status_code == 429:
        raise Exception("Rate limit")
