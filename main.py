import logging
import sqlite3
import types
import time
import asyncio

import executor
from aiogram import Bot, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


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


@dp.message(Command('start'))
async def start(message: Message):
    kb = [
        [
            [types.KeyboardButton(text="Дэвы/Разработка", callback_data='dev')],
            [types.KeyboardButton(text="Администрирование Windows", callback_data='windows')],
            [types.KeyboardButton(text="Практические задания Linux/bsd", callback_data='lin')],
            [types.KeyboardButton(text="Проекты ИБ Безопасность", callback_data='ib')]
            [types.KeyboardButton(text="Просто Практика", callback_data='ib')]
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await message.answer("Выбери направление", reply_markup=keyboard)


@dp.callback_query(lambda c: c.data == 'dev')
async def sev(callback_query: types.CallbackQuery):
    adkb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    adkb.add(types.ReplyKeyboardMarkup(text="1001 Просмотр пакетов при авторизации wireshark ", callback_data='1001'))
    adkb.add(types.ReplyKeyboardMarkup(text="1002 Перехватить wifi ", callback_data='1002'))
    adkb.add(types.ReplyKeyboardMarkup(
        text="1003 Произвести сканирование сайта и разобрать отчёт \n по найденным уязвимостям openVAs,либо nessus ",
        callback_data='1003'))
    adkb.add(types.ReplyKeyboardMarkup(text="1004 сформировать таблицу IP адресов в файле на основе обращений",
                                       callback_data='1004'))
    bbt = types.KeyboardButton(text='Выбери задание', request_contact=True)
    adkb.add(bbt)
    await bot.send_photo(callback_query.from_user.id, "Привет")
    await dialog.send_contact_IB.set()


@dp.callback_query(lambda c: c.data == 'windows')
async def win(callback_query: types.CallbackQuery):
    adkb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    adkb.add(types.ReplyKeyboardMarkup(text="1001 Просмотр пакетов при авторизации wireshark ", callback_data='1001'))
    adkb.add(types.ReplyKeyboardMarkup(text="1002 Перехватить wifi ", callback_data='1002'))
    adkb.add(types.ReplyKeyboardMarkup(
        text="1003 Произвести сканирование сайта и разобрать отчёт \n по найденным уязвимостям openVAs,либо nessus ",
        callback_data='1003'))
    adkb.add(types.ReplyKeyboardMarkup(text="1004 сформировать таблицу IP адресов в файле на основе обращений",
                                       callback_data='1004'))
    bbt = types.KeyboardButton(text='Выбери задание', request_contact=True)
    adkb.add(bbt)
    await bot.send_photo(callback_query.from_user.id, "Привет")
    await dialog.send_contact_IB.set()


@dp.callback_query(lambda c: c.data == 'linux')
async def linux(callback_query: types.CallbackQuery):
    adkb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    adkb.add(types.ReplyKeyboardMarkup(text="1001 Просмотр пакетов при авторизации wireshark ", callback_data='1001'))
    adkb.add(types.ReplyKeyboardMarkup(text="1002 Перехватить wifi ", callback_data='1002'))
    adkb.add(types.ReplyKeyboardMarkup(
        text="1003 Произвести сканирование сайта и разобрать отчёт \n по найденным уязвимостям openVAs,либо nessus ",
        callback_data='1003'))
    adkb.add(types.ReplyKeyboardMarkup(text="1004 сформировать таблицу IP адресов в файле на основе обращений",
                                       callback_data='1004'))
    bbt = types.KeyboardButton(text='Выбери задание', request_contact=True)
    adkb.add(bbt)
    await bot.send_photo(callback_query.from_user.id, "Привет")
    await dialog.send_contact_IB.set()


@dp.callback_query(lambda c: c.data == 'IB')
async def IB(callback_query: types.CallbackQuery):
    adkb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    adkb.add(types.ReplyKeyboardMarkup(text="1001 Просмотр пакетов при авторизации wireshark ", callback_data='1001'))
    adkb.add(types.ReplyKeyboardMarkup(text="1002 Перехватить wifi ", callback_data='1002'))
    adkb.add(types.ReplyKeyboardMarkup(text="1003 Произвести сканирование сайта и разобрать отчёт \n по найденным уязвимостям openVAs,либо nessus ", callback_data='1003'))
    adkb.add(types.ReplyKeyboardMarkup(text="1004 сформировать таблицу IP адресов в файле на основе обращений", callback_data='1004'))
    bbt = types.KeyboardButton(text='Выбери задание', request_contact=True)
    adkb.add(bbt)
    await bot.send_photo(callback_query.from_user.id, "Привет")
    await dialog.send_contact_IB.set()

""""
@dp.message(state=dialog.send_contact_dev, content_types=types.ContentType.CONTACT)
async def proc(message: types.Message, state: FSMContext):
    await bot.send_contact(OLEG, first_name=message.contact.first_name, last_name=message.contact.last_name, phone_number=message.contact.phone_number)
    await bot.send_message(OLEG, text="dev")
    await state.finish()

@dp.message(state=dialog.send_contact_win, content_types=types.ContentType.CONTACT)
async def proc(message: types.Message, state: FSMContext):
    await bot.send_contact(OLEG, first_name=message.contact.first_name, last_name=message.contact.last_name, phone_number=message.contact.phone_number)
    await bot.send_message(OLEG, text="win")
    await state.finish()

@dp.message(state=dialog.send_contact_IB, content_types=types.ContentType.CONTACT)
async def proc(message: types.Message, state: FSMContext):
    await bot.send_contact(ADMIN, first_name=message.contact.first_name, last_name=message.contact.last_name, phone_number=message.contact.phone_number)
    await bot.send_message(ADMIN, text="IB")
    await state.finish()

@dp.message(state=dialog.send_contact_lin, content_types=types.ContentType.CONTACT)
async def proc(message: types.Message, state: FSMContext):
    await bot.send_contact(OLEG, first_name=message.contact.first_name, last_name=message.contact.last_name, phone_number=message.contact.phone_number)
    await bot.send_message(OLEG, text="linux")
    await state.finish()
"""


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
if __name__ == '__main__':
    #executor.start_polling(dp, skip_updates=True)
    #logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    #asyncio.run(main())
    asyncio.run(main())