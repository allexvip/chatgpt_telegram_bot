import aiogram
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import os
import logging
import translators as ts
import translators.server as tss
import requests

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_API_KEY")

# Инициализация бота и диспетчера
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    filename="bot.log",
)


# Хэндлер на команду /start , /help
@dp.message_handler(commands=["start", "help"])
async def cmd_start(message: types.Message):
    await message.reply(
        """Привет! Я бот способный отвечать на вопросы. 
Каждый вопрос ботом переводится на английский язык и затем задаётся сайту you.com
Создатель бота не несёт ответственности за предоставленные ботом ответы с сайта you.com"""
    )


# Хэндлер на получение текста
@dp.message_handler(content_types=[types.ContentType.TEXT])
async def cmd_text(message: types.Message):
    """
    Обработчик на получение текста
    """
    # await bot.send_chat_action(message.from_user.id,"choose_sticker")
    await bot.send_chat_action(message.from_user.id, "typing")
    betterapi_token = os.getenv("BETTERAPI_TOKEN")
    input_msg = message.text
    input_message = tss.google(input_msg, 'ru', 'en')
    print(message.text, input_message)
    data = requests.get(
        f"https://api.betterapi.net/youdotcom/chat?message={input_message}&key={betterapi_token}").json()
    # print(data)
    msg = ""
    try:
        if data['message']:
            msg = tss.google(data['message'], 'en', 'ru')
            # print(data['message'], msg)
        else:
            await message.reply(f"""you.com:

Я не знаю.""")
    except:
        msg = "got an error!"
    await message.reply(f"""you.com:

{msg}""")


# Запуск цикла обработки сообщений
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)
