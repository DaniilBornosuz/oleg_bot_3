import logging
import sqlite3
import types
import time

import executor
from aiogram import Bot, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode
#import aiogram
#from aiogram.types import InputFile, ContentType
#from aiogram import Bot, Dispatcher, executor, types
#from aiogram.contrib.fsm_storage.memory import MemoryStorage
#from aiogram.dispatcher import FSMContext
#from aiogram.bot.api import TelegramAPIServer
#from aiogram.dispatcher.filters.state import State, StatesGroup
#from aiogram.types import Message, InlineKeyboardButton, contact
#from aiogram.utils.exceptions import (MessageToEditNotFound, MessageCantBeEdited, MessageCantBeDeleted,
                                     # MessageToDeleteNotFound)

API_TOKEN = '6976515071:AAEoQKuWyo5IpuW257iJex-A2hCAfSxY_VQ'
ADMIN = 417905942
OLEG = 498487337
oleg_chat_id = 0
user_data = {}
#local_server=TelegramAPIServer.from_base('http://localhos')
date = time.strftime('%Y-%m-%d %H-%M')
logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)
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


@dp.message(Command['start'])
async def start(message: Message):
    adkb = types.InlineKeyboardMarkup(resize_keyboard=True)
    adkb.add(types.InlineKeyboardButton(text="Дэвы/Разработка", callback_data='dev'))
    adkb.add(types.InlineKeyboardButton(text="Администрирование Windows", callback_data='windows'))
    adkb.add(types.InlineKeyboardButton(text="Практические задания Linux/bsd", callback_data='linux'))
    adkb.add(types.InlineKeyboardButton(text="Проекты ИБ Безопасность", callback_data='IB'))
    adkb.add(types.InlineKeyboardButton(text="Мне просто сделать документы по практике", callback_data='lazy'))
    await message.answer('Выбери специальность', reply_markup=adkb)


@dp.callback_query_handler(lambda c: c.data == 'dev')
async def sev(callback_query: types.CallbackQuery):
    kkb = types.ReplyKeyboardMarkup()
    bbt = types.KeyboardButton('Отправить контакт', request_contact=True)
    kkb.add(bbt)
    await bot.send_message(callback_query.from_user.id,
                           'http://glpi.mintrans.gov.ru:19223/front/project.form.php?id=77',reply_markup=kkb)
    await bot.send_photo(callback_query.from_user.id ,"photo/dev.jpeg",reply_markup=kkb)
    await bot.send_message(callback_query.from_user.id,"Отправь карточку контакта")
    await dialog.send_contact_dev.set()


@dp.callback_query_handler(lambda c: c.data == 'windows')
async def win(callback_query: types.CallbackQuery):
    kkb = types.ReplyKeyboardMarkup()
    bbt = types.KeyboardButton('Отправить контакт', request_contact=True)
    kkb.add(bbt)
    await bot.send_message(callback_query.from_user.id,
                           'http://glpi.mintrans.gov.ru:19223/front/project.form.php?id=78',reply_markup=kkb)
    await bot.send_message(callback_query.from_user.id,"Отправь карточку контакта")
    await dialog.send_contact_win.set()


@dp.callback_query_handler(lambda c: c.data == 'linux')
async def linux(callback_query: types.CallbackQuery):
    kkb = types.ReplyKeyboardMarkup()
    bbt = types.KeyboardButton('Отправить контакт', request_contact=True)
    kkb.add(bbt)
    await bot.send_message(callback_query.from_user.id,
                           'http://glpi.mintrans.gov.ru:19223/front/project.form.php?id=74',reply_markup=kkb)

    await bot.send_message(callback_query.from_user.id,"Отправь карточку контакта")
    await dialog.send_contact_lin.set()


@dp.callback_query_handler(lambda c: c.data == 'IB')
async def IB(callback_query: types.CallbackQuery):
    adkb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    adkb.add(types.ReplyKeyboardMarkup(text="1001 Просмотр пакетов при авторизации wireshark ", callback_data='1001'))
    adkb.add(types.ReplyKeyboardMarkup(text="1002 Перехватить wifi ", callback_data='1002'))
    adkb.add(types.ReplyKeyboardMarkup(text="1003 Произвести сканирование сайта и разобрать отчёт \n по найденным уязвимостям openVAs,либо nessus ", callback_data='1003'))
    adkb.add(types.ReplyKeyboardMarkup(text="1004 сформировать таблицу IP адресов в файле на основе обращений", callback_data='1004'))
    bbt = types.KeyboardButton('Выбери задание', request_contact=True)
    adkb.add(bbt)
    #await bot.send_photo(callback_query.from_user.id, "AgACAgIAAxkBAAIBE2V0eaOZbhnP1mXnSfYzWkQ57z8IAAKe1DEb6oapSwdSJ15WxfkWAQADAgADeQADMwQ")
    await dialog.send_contact_IB.set()


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

@dp.message(content_types=['photo'])
async def get_file_id_p(message: types.Message):
    await message.reply(message.photo[-1].file_id)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
