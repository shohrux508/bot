from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from aiogram import types

from loader import bot
from utils.db_api.manage import ManageUser


class BigBrother(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        if update.message:
            ID = update.message.from_user.id
            if update.message.text in ['/start', '/help']:
                return
        elif update.callback_query:
            ID = update.callback_query.from_user.id
            if update.callback_query.data == f'check+{ID}':
                return
        else:
            return
        if ManageUser(ID).is_blocked():
            await bot.send_message(chat_id=update.message.from_user.id, text='Вы заблокированы!')
            raise CancelHandler()

