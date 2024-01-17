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


router = Router()

class MyCallback(CallbackData, prefix="my"):
  spec: str
  num: int

class UserAction(CallbackData, prefix="user_action"):
  click: str

""" Обработка нажатия Inline кнопки 1 """
@router.callback_query(UserAction.filter(F.click == "1"))
async def practice_and_employment(call: CallbackQuery, callback_data: UserAction, state: FSMContext, bot: Bot) -> None:
  # Обновляем данные состояния
  await state.update_data(user_intent=callback_data.click)
  # Устанавливаем следующее состояние
  await state.set_state(FSMDialog.chosie_task)

  category_task_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
      InlineKeyboardButton(text=text_kb.dev, callback_data=MyCallback(spec="dev", num=20).pack())
    ],
    [
      InlineKeyboardButton(text=text_kb.win, callback_data=MyCallback(spec="win", num=30).pack())
    ],
    [
      InlineKeyboardButton(text=text_kb.lin, callback_data=MyCallback(spec="lin", num=00).pack())
    ],
    [
      InlineKeyboardButton(text=text_kb.ib, callback_data=MyCallback(spec="ib", num=10).pack())
    ],
    [
      InlineKeyboardButton(text=text_kb.back, callback_data=UserAction(click="back").pack())
    ]
  ])
  
  await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
  await call.message.answer("Вы выбрали практика с трудоустройством", reply_markup=category_task_kb)
  await call.answer()


""" Обработка нажатия Inline кнопки 2 """
@router.callback_query(UserAction.filter(F.click == "2"))
async def practice(call: CallbackQuery, callback_data: UserAction, state: FSMContext, bot: Bot) -> None:
  kb = [
    [
      KeyboardButton(text=text_kb.contact, request_contact=True)
    ],
  ]
  send_contact_kb = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
  await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
  
  await state.set_state(state=FSMDialog.send_contact)
  await call.message.answer("Вы выбрали просто практика.\nОтправьте свой контакт для связи.\nПодписать документы можно по адресу: Улица Пушкина дом кукушкина", reply_markup=send_contact_kb)
  await call.answer()


""" Обработка нажатия Inline кнопки назад """
@router.callback_query(UserAction.filter(F.click == "back"))
async def go_back(call: CallbackQuery, callback_data: UserAction, state: FSMContext, bot: Bot):
  # Проверяем какой стейт был последним для данного пользователя