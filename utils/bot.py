from telegram import Bot
from utils.config import load_config


async def send_message( message, parse_mode='HTML'):
    bot = Bot(token=load_config('auth_token'))
    await bot.send_message(chat_id=load_config('chat_id'), text=message, parse_mode=parse_mode)