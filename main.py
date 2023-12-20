import logging
import os
import sqlite3
import types
import time
import asyncio
import random

import executor
from aiogram import F
from aiogram import Bot, Dispatcher
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from pathlib import Path
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.handlers import CallbackQueryHandler
from aiogram.utils.keyboard import InlineKeyboardBuilder

API_TOKEN = '6989160606:AAEbRp9yoEH1U3x8Yq1y61SWrK0dvZixAew'
ADMIN = 417905942
OLEG = 498487337
oleg_chat_id = 0
user_data = {}

date = time.strftime('%Y-%m-%d %H-%M')
logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(token=API_TOKEN, storage=storage)
conn = sqlite3.connect('db.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users(user_id INTEGER, block INTEGER);""")
conn.commit()

class dialog(StatesGroup):
    send_info = State()
    chosie_task = State()
    send_contact_dev = State()
    send_contact_win = State()
    send_contact_IB = State()
    send_contact_lin = State()

class MyCallback(CallbackData, prefix="my"):
    spec: 'str'
    num: 'int'
class push_button(CallbackData, prefix="fuck"):
    click: 'str'

@dp.message(Command('start'))
async def start(message: Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Девы и разработка",callback_data=MyCallback(spec="dev",num="200").pack())),
    builder.add(types.InlineKeyboardButton(text="Администрирование Windows", callback_data=MyCallback(spec="win",num="300").pack())),
    builder.add(types.InlineKeyboardButton(text="Практические задания Linux/bsd", callback_data=MyCallback(spec="lin",num="000").pack())),
    builder.add(types.InlineKeyboardButton(text="Проекты ИБ Безопасность", callback_data=MyCallback(spec="ib",num="100").pack())),
    builder.add(types.InlineKeyboardButton(text="Просто Практика", callback_data='loh'))
    await message.answer("Выбери направление",reply_markup=builder.as_markup())

@dp.callback_query(MyCallback.filter(F.spec))
async def sev(query: CallbackQuery, callback_data: MyCallback):
    global list, dir,name,a
    a = 1
    dir = callback_data.spec
    name = callback_data.num
    list = os.listdir(dir)
    print(list)
    with open(f"{callback_data.spec}/{name}{a}.txt") as file:
        task = file.read()
        print(task)
        global builder
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Берусь", callback_data=push_button(click='yes').pack()))
    builder.add(types.InlineKeyboardButton(text="<<", callback_data=push_button(click='<<').pack()))
    builder.add(types.InlineKeyboardButton(text=">>", callback_data=push_button(click='>>').pack()))
    builder.add(types.InlineKeyboardButton(text="назад",callback_data=push_button(click='end').pack()))

    await query.message.edit_text(text=task, reply_markup=builder.as_markup())
    return dir,name

@dp.callback_query(push_button.filter(F.click))
async def button(query: CallbackQuery,callback_data: push_button):
    print(callback_data.click)
    print(push_button)
    a = len(list)
    #for i in range(len(list)):
    if (callback_data.click == ">>"):
        a = random.randint(1, a)
        """
        ни как не мог вспомнить ка делать блядский перебор вот и поставил рандом 
        кому не нравится идите нахуй мой бот че хочу то и делаю 
        захочу назову переменную хуй
        """
        print(a)
        with open(f"{dir}/{name}{a}.txt") as file:
            task = file.read()
        await query.message.edit_text(text=task,reply_markup=builder.as_markup())
    if (callback_data.click == "<<"):
        a = a+1
        with open(f"{dir}/{name}{a}.txt") as file:
            task = file.read()
        await query.message.edit_text(text=task,reply_markup=builder.as_markup())
    if (callback_data.click == "end"):
        await query.message.answer("Для открытия меню отправьте /start")
        await query.message.delete()

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
if __name__ == '__main__':
    asyncio.run(main())