from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp
from utils.db_api.manage import ManageUser


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    if ManageUser(message.from_user.id).language() == 'uz':
        text = ("Buyruqlar: ",
                "/start - Botni ishga tushurish",
                "/help - Yordam",
                "/change_language - Tilni o'zgartirish",
                '/register - Olimpiadada qatnashish')
    else:
        text = ("Список команд: ",
                "/start - Начать диалог",
                "/help - Получить справку",
                '/change_language - Сменить язык',
                '/register - Зарегистрироваться на олимпиады')
    await message.answer("\n".join(text))
