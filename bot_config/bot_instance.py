from settings import settings
from bot_config.telegram_client import CompanyBot, telegram_client
from aiogram import Dispatcher

bot = CompanyBot(token=settings.bot_token, telegram_client=telegram_client)
dp = Dispatcher()
