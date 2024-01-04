from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.default.admin import AdminKeyboard
from utils.db_api.manage import ManageUser, Check


def button(text, data, func):
    user_id = (data.split("+")[0])
    kb = InlineKeyboardButton(text=text, callback_data=func + data)
    keyboard = InlineKeyboardMarkup().add(kb)
    if func == 'answer' and not ManageUser(user_id).is_admin():
        keyboard.add(InlineKeyboardButton(text='Найти пользователя🔍', callback_data=f'find_user{user_id}'))
    return keyboard

def url_button(title, url):
    btn = InlineKeyboardButton(text=title, url=url)
    return InlineKeyboardMarkup().add(btn)


def keyboards(list):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(*list)
    return keyboard


def _keyboard(*args):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(*args)
    return keyboard
