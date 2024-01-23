import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from core.handlers.basic import get_start
from core.utils.commands import set_command
from core.handlers.callback import practice, practice_and_employment
from core.handlers import basic, callback
from core.db.database import sql_start 

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

router = Router()

""" Отправка сообщения админу при запуске бота """
async def start_bot(bot: Bot):
  await set_command(bot)
  await bot.send_message(ADMIN_ID, text="Бот запущен!")

""" Отправка сообщения админу при остановке бота """
async def stop_bot(bot: Bot):
  await bot.send_message(ADMIN_ID, text="Бот остановлен!")


async def main() -> None:
  bot = Bot(token=BOT_TOKEN)
  storage = MemoryStorage()
  dp = Dispatcher(token=BOT_TOKEN, storage=storage)

  dp.startup.register(start_bot)
  dp.shutdown.register(stop_bot)

  dp.include_routers(basic.router, callback.router)

  sql_start()
  try:
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
  finally:
    bot.session.close()   


if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO)
  asyncio.run(main())