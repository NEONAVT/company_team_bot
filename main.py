from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery

from settings import settings
import asyncio

bot = Bot(settings.bot_token)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(f"Hello {message.from_user.first_name}!")

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))