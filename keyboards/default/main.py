from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from keyboards.default.admin import AdminKeyboard
from keyboards.default.user import UserKeyboard
from utils.db_api.manage import ManageUser


class StartKeyboard():
    def __init__(self, user_id):
        self.user_id = user_id

    def keyboard(self):
        if ManageUser(user_id=self.user_id).is_admin():
            return AdminKeyboard().main()
        else:
            lang = ManageUser(self.user_id).language()
            return UserKeyboard(self.user_id, lang).main()


class OneTimeKeyboards():
    def __init__(self, user_id):
        self.user_id = user_id

    def share_phone(self):
        if ManageUser(self.user_id).language() == 'uz':
            kb = KeyboardButton(text='Ulashish', request_contact=True)
        else:
            kb = KeyboardButton(text='Поделиться', request_contact=True)
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(kb)
        return keyboard

    def share_location(self):
        if ManageUser(self.user_id).language() == 'uz':
            kb = KeyboardButton(text='Ulashish', request_location=True)
        else:
            kb = KeyboardButton(text='Поделиться', request_location=True)
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(kb)
        return keyboard
