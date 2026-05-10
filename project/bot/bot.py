import os
import aiohttp
import logging
logging.basicConfig(level=logging.INFO)


from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
BACKEND_URL = os.getenv("BACKEND_URL", "http://rag-nginx/ask")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["history"])
async def history_handler(message: types.Message):
    user_id = message.from_user.id

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BACKEND_URL}/history/{user_id}") as resp:
            data = await resp.json()

    if not data:
        await message.answer("История пуста.")
        return

    text = "Ваши последние запросы:\n\n"
    for item in data[:10]:
        text += f"❓ {item['question']}\n"
        text += f"💬 {item['answer']}\n\n"

    await message.answer(text)

@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def handle_message(message: types.Message):
    print(f"Received message: {message.text}")
    chat_id = message.chat.id
    user_id = message.from_user.id
    question = message.text

    async with aiohttp.ClientSession() as session:
        await session.post(
            BACKEND_URL,
            json={
                "question": question,
                "chat_id": chat_id,
                "user_id": user_id
            }
        )

    await message.answer("Ваш вопрос принят. Я пришлю ответ, как только он будет готов.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
