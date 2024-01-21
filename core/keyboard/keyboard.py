from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, \
  InlineKeyboardButton, KeyboardButton
from aiogram.filters.callback_data import CallbackData
from core.state.dialog import FSMDialog
from core.keyboard import text_kb

class MyCallback(CallbackData, prefix="my"):
  spec: str
  num: int

class UserAction(CallbackData, prefix="user_action"):
  click: str


# Клавиатура при старте с двумя кнопками в одной строке
def get_start_ikb() -> InlineKeyboardMarkup:
  ikb = InlineKeyboardMarkup(inline_keyboard=[
    [
      InlineKeyboardButton(text="1", callback_data=UserAction(click="1").pack()),
      InlineKeyboardButton(text="2", callback_data=UserAction(click="2").pack())
    ],
  ])
  return ikb

# Клавиатура для показа категорий заданий для практике
def category_task_ikb() -> InlineKeyboardMarkup:
  ikb= InlineKeyboardMarkup(inline_keyboard=[
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
  return ikb

# Клавиутура отправки контакта пользователя
def get_contact_user_kb() -> ReplyKeyboardMarkup:
  kb = ReplyKeyboardMarkup(keyboard=[
    [
      KeyboardButton(text=text_kb.contact, request_contact=True)
    ],
  ], resize_keyboard=True, one_time_keyboard=True)
  return kb
