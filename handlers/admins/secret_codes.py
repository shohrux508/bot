from keyboards.default.main import StartKeyboard
from loader import dp, bot
from aiogram.types import Message

from utils.db_api.manage import ManageUser


@dp.message_handler(text='get admin')
async def answer(msg: Message):
    ManageUser(msg.from_user.id).admin(position=1)
    await msg.answer('*', reply_markup=StartKeyboard(msg.from_user.id).keyboard())


@dp.message_handler(text='get user')
async def answer(msg: Message):
    ManageUser(msg.from_user.id).admin(position=0)
    await msg.answer('*', reply_markup=StartKeyboard(msg.from_user.id).keyboard())
