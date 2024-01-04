from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from utils.db_api.manage import DirectionManager


class UserKeyboard():
    def __init__(self, user_id, language):
        self.user_id = user_id
        self.language = language

    def main(self):
        if self.language == 'ru':
            kb2 = KeyboardButton(text='Олимпиада')
            kb3 = KeyboardButton(text='Обратная связь')
            kb4 = KeyboardButton(text='Образцы для подготовки')
            kb5 = KeyboardButton(text='Рекомендации по улучшению бота')
            kb6 = KeyboardButton(text='Видеоуроки')
        else:
            kb2 = KeyboardButton(text='Olimpiada')
            kb3 = KeyboardButton(text='Qayta aloqa')
            kb4 = KeyboardButton(text='Tayyorlanish uchun masalalar')
            kb5 = KeyboardButton(text='Taklif bildirish')
            kb6 = KeyboardButton(text='Videodarslar')

        keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(kb2, kb4).add(kb3, kb5).add(kb6)
        return keyboard

    def programming_languages(self):
        datas = DirectionManager().list(select_title=True)
        btn_list = []
        for i in datas:
            btn = KeyboardButton(text=i[0])
            btn_list.append(btn)
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(*btn_list).add(home_btn, back_btn)
        return keyboard


def webb():
    web_app = WebAppInfo(url='https://127.0.0.1:8000/telegram/welcome/')
    kb = KeyboardButton(text='Открыть', web_app=web_app)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(kb)
    return keyboard
