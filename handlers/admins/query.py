from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.one_time_keyboards import button
from loader import dp, bot
from shortcuts.main_shortcuts import filter_data, manage_user_kb
from states.StatesGroup import Chat
from utils.db_api.manage import ManageUser, search_user


# admin/disadmin
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('admin'))
async def set_admin(call: CallbackQuery):
    try:
        position, user_id = (filter_data(call.data, 'admin')).split('+')
        ManageUser(user_id).admin(position)
        user_id, text = search_user(user_id)
        await bot.edit_message_text(chat_id=call.from_user.id, text=text, message_id=call.message.message_id,
                                    reply_markup=manage_user_kb(user_id, call.from_user.id))
        await call.answer('Успешно!')
    except:
        await call.answer('Ошибка, не удалось внесить изменения!')


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('ban'))
async def set_block(call: CallbackQuery):
    try:
        status, user_id = (filter_data(call.data, 'ban')).split('+')
        ManageUser(user_id).block(status)
        user_id, text = search_user(user_id)
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text,
                                    reply_markup=manage_user_kb(user_id, call.from_user.id))
        await call.answer('Успешно')
    except:
        await call.answer('Ошибка, Не удалось внесить изменения!')


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('sent_message_to_user'))
async def sent_message(call: CallbackQuery, state: FSMContext):
    user_id = filter_data(call.data, 'send_message_to_user')
    await state.update_data(user_id=user_id)
    await state.set_state(Chat.get_private_msg_to_user.state)
    await bot.send_message(chat_id='Введите текст сообщения!\n'
                                   'Отменить: /break')


@dp.message_handler(state=Chat.get_private_msg_to_user.state)
async def send_message(msg: Message, state: FSMContext):
    if 'break' in msg.text:
        await state.finish()
        await msg.answer('Отменено!')
        return
    user_id = await state.get_data('user_id')
    try:
        await bot.send_message(chat_id=user_id, text=msg.text,
                               reply_markup=button('Ответить', f'{user_id}+{msg.message_id}', 'answer'))
    except:
        await msg.answer('Не удалось отправить сообщение!')



