from telegram import Bot
from utils.config import load_config
from utils.logger import logger


async def send_message( message, parse_mode='HTML'):
    if load_config('bot_notif') and load_config('chat_id') is not None:
        try:
            bot = Bot(token=load_config('auth_token'))
            await bot.send_message(chat_id=load_config('chat_id'), text=message, parse_mode=parse_mode)
        except Exception as e:
            logger.error(f"Message Error: {str(e)}")

    else:
        logger.warning("Chat Bot False or Chat ID None. Please set the chat ID or Chat Bot in the config.json file.")