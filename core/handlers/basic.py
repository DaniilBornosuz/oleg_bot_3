import asyncio 
from aiogram import Bot, Router, Dispatcher
from aiogram import F
from aiogram import types
from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardButton, \
  InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, CommandStart
from core.keyboard import text_kb
from core.keyboard.keyboard import get_start_ikb

from core.state.dialog import FSMDialog
from core.handlers.callback import UserAction


router = Router()

""" Общая команда старта """
@router.message(CommandStart())
async def get_start(message: Message, bot: Bot, state: FSMContext) -> None:
  # Устанавливаем состояние 
  await state.set_state(FSMDialog.user_intent)

  message_text = (
    f"Привет {message.from_user.username}, что тебя интересует?\n"
    "1.Практика с трудоустройством\n"
    "2.Просто практика."
  )

  await bot.send_message(
    message.from_user.id, 
    message_text, 
    reply_markup=get_start_ikb())
  # Удаляем сообщение 
  await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


""" Ответ на получение контакта пользователя """
@router.message(F.contact)
async def get_contacts(message: Message, state: FSMContext, bot: Bot) -> None:
  await state.update_data(get_contact = message.contact.phone_number)
  
  # Получаем текущий стейт
  current_state = await state.get_state()
  current_state_data = await state.get_data()
  print(f"Текущий sate: {current_state}")
  print(current_state_data)

  message_text = (f"Твой номер успешно получен: {message.contact.phone_number}")
  await message.answer(message_text, reply_markup=ReplyKeyboardRemove())
  # Нужно сохранить контакт пользователя и прочую информацию




