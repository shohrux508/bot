from aiogram import types

from utils.db_api.manage import ManageUser


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand('menu', 'Menu')
        ]

    )
