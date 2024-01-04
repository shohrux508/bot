from aiogram import Bot

from data.database import *
from typing import Union
from utils.db_api.manage import ManageUser


def is_required(channel_id):
    cur.execute(f'''SELECT is_required FROM channels WHERE channel_id = {channel_id}''')
    response = cur.fetchone()
    data = response[0]
    if data == 1:
        return True
    else:
        return False


async def is_member(user_id, channel: Union[int, str]):
    if ManageUser(user_id).is_admin():
        return True
    else:
        bot = Bot.get_current()
        member = await bot.get_chat_member(user_id=user_id, chat_id=channel)
        return member.is_chat_member()
