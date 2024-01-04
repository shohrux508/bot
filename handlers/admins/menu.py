from loader import bot, dp
from aiogram.types import CallbackQuery, Message

from utils.db_api.manage import ManageUser


@dp.message_handler(commands='menu')
async def answer(msg: Message):
    if ManageUser(msg.from_user.id).is_admin():
        menu = (f'Запустить бота: /start\n'
                f'Скачать список пользователей: /get_users_as_excel\n'
                f'Языки программирования: /directions\n'
                f'Образцы для подготовки: /examples\n'
                f'Факультеты: /faculties\n')
        await msg.answer(menu)
    else:
        if ManageUser(msg.from_user.id).language() == 'uz':
            menu = (f'Botni ishga tushurish: /start\n'
                    f'Yordam: /help\n'
                    f"Tilni o'zgartirish: /change_language\n"
                    f"Ro'yxatdan o'tish: /register")
        else:
            menu = (f'Запустить бота: /start\n'
                    f'Помощь: /help\n'
                    f'Смена языка: /change_language\n'
                    f'Зарегистрироваться: /register')
        await msg.answer(menu)
