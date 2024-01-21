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
  # Удаляем сообщение 
  await bot.send_message(
    message.from_user.id, 
    f"Привет {message.from_user.username}, что тебя интересует?\n1.Практика с трудоустройством\n2.Просто практика.", 
    reply_markup=get_start_ikb())
  await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


""" Ответ на получение контакта пользователя """
@router.message(lambda message: message.text == text_kb.contact )
async def get_contacts(message: Message, state: FSMContext) -> None:
  # Получаем текущий стейт
  current_state = await state.get_state()
  if current_state == "send_contact":
    contact = message.contact
    await state.update_data()
    
    await state.finish()
    await message.answer(f"Твой номер успешно получен: {contact.phone_number}", reply_markup=ReplyKeyboardRemove())
  # Нужно сохранить контакт пользователя и прочую информацию




