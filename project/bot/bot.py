import os
import aiohttp
import logging
logging.basicConfig(level=logging.INFO)


from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
BACKEND_URL = os.getenv("BACKEND_URL", "http://rag-nginx")

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.answer(
        "Привет! 👋\n\n"
        "Я готов помочь.\n"
        "По возможности задавайте вопросы на английском — так ответы будут точнее.\n\n"
        "Доступные команды:\n"
        "/start — приветствие\n"
        "/history — последние вопросы\n"
        "/help — помощь\n\n"
        "Можете начать прямо сейчас!"
    )


@dp.message_handler(commands=["help"])
async def help_handler(message: types.Message):
    await message.answer(
        "📘 *Справка*\n\n"
        "Доступные команды:\n"
        "/start — приветствие\n"
        "/history — последние вопросы\n"
        "/help — помощь\n\n"
        "Просто напишите свой вопрос, и я отправлю его на обработку."
    )


@dp.message_handler(commands=["history"])
async def history_handler(message: types.Message):
    user_id = message.from_user.id

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{BACKEND_URL}/history/{user_id}") as resp:
            data = await resp.json()

    if not data:
        await message.answer("История пуста.")
        return

    text = "Ваши последние вопросы:\n\n"

    for item in data[:10]:
        q = item["question"]

        if len(q) > 200:
            q = q[:200] + "..."

        text += f"❓ {q}\n\n"

    if len(text) > 3500:
        text = text[:3500] + "\n\n(История обрезана)"

    await message.answer(text)


@dp.message_handler(lambda msg: msg.text.startswith("/"))
async def unknown_command(message: types.Message):
    await message.answer(
        "Неизвестная команда. Используйте /help, чтобы посмотреть доступные команды."
    )


@dp.message_handler(lambda msg: not msg.text.startswith("/"), content_types=types.ContentTypes.TEXT)
async def handle_message(message: types.Message):
    print(f"Received message: {message.text}")
    chat_id = message.chat.id
    user_id = message.from_user.id
    question = message.text.strip()
    message_id = message.message_id

 
    if len(question) < 3:
        await message.answer("Сообщение слишком короткое, опишите подробнее ваш вопрос.")
        return

    async with aiohttp.ClientSession() as session:
        await session.post(
            f"{BACKEND_URL}/ask",
            json={
                "question": question,
                "chat_id": chat_id,
                "user_id": user_id,
                "message_id": message_id
            }
        )

    await message.answer("Ваш вопрос принят. Я пришлю ответ, как только он будет готов.")

if __name__ == "__main__":
    print("Bot started!")
    executor.start_polling(dp, skip_updates=True)