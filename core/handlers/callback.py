import asyncio
from aiogram import Bot, Router, Dispatcher
from aiogram import F 
from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardButton, \
  InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from core.keyboard import text_kb
from aiogram.methods.send_contact import SendContact
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from core.state.dialog import FSMDialog
from core.keyboard.keyboard import UserAction, MyCallback, \
  category_task_ikb, get_contact_user_kb, get_start_ikb

router = Router()



""" Обработка нажатия Inline кнопки 1 """
@router.callback_query(UserAction.filter(F.click == "1"))
async def practice_and_employment(call: CallbackQuery, callback_data: UserAction, state: FSMContext, bot: Bot) -> None:
  # Обновляем данные состояния
  await state.update_data(user_intent=callback_data.click)
  # Устанавливаем следующее состояние
  await state.set_state(FSMDialog.chosie_task)

  current_state = await state.get_state()
  current_state_data = await state.get_data()
  print(f"Текущий sate: {current_state}")
  print(current_state_data)

  message_text = ("Вы выбрали практика с трудоустройством")
  
  await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
  await call.message.answer(message_text, reply_markup=category_task_ikb())
  await call.answer() # Обработка inline кнопки чтоб не показывались часики


""" Обработка нажатия Inline кнопки 2 """
@router.callback_query(UserAction.filter(F.click == "2"))
async def practice(call: CallbackQuery, callback_data: UserAction, state: FSMContext, bot: Bot) -> None:
  await state.update_data(state.update_data == call.message.text)
  await state.set_state(state=FSMDialog.send_contact)
  
  current_state = await state.get_state()
  current_state_data = await state.get_data()
  print(f"Текущий sate: {current_state}")
  print(current_state_data)

  message_text = (
    "Вы выбрали просто практика.\n"
    "Отправьте свой контакт для связи.\n"
    "Подписать документы можно по адресу: ул. Первомайская, 76, Москва, 105554"
  )

  await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
  await call.message.answer(message_text, reply_markup=get_contact_user_kb())
  await call.message.answer_location(latitude=55.792883, longitude=37.801961, horizontal_accuracy=200.0)
  await call.answer()


""" Обработка нажатия Inline кнопки назад """
@router.callback_query(UserAction.filter(F.click == "back"))
async def go_back(call: CallbackQuery, callback_data: UserAction, state: FSMContext, bot: Bot):
  await state.set_state(state=FSMDialog.user_intent)

  current_state = await state.get_state()
  current_state_data = await state.get_data()
  print(f"Текущий sate: {current_state}")
  print(current_state_data)

  message_text = ( 
    "Привет, что тебя интересует?\n"
    "1.Практика с трудоустройством\n"
    "2.Просто практика."
  )

  await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
  await call.message.answer(
    text=message_text,  
    reply_markup=get_start_ikb())
  await call.answer()
