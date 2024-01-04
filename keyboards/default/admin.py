from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


back_kb = KeyboardButton(text='Назад🔙')
home_kb = KeyboardButton(text='🏠Главное')


class AdminKeyboard():
    def main(self):
        kb1 = KeyboardButton(text='Отправить сообщение')
        kb2 = KeyboardButton(text='Пользователи')
        kb3 = KeyboardButton(text='Каналы')
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(kb1, kb2).add(kb3)
        return keyboard

    def channels(self):
        kb1 = KeyboardButton(text='Добавить канал ➕')
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(kb1).add(home_kb, back_kb)
        return keyboard
