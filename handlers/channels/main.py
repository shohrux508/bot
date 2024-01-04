from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, Message

from keyboards.inline.admin import AdminButton
from keyboards.one_time_keyboards import button
from loader import dp, bot
from shortcuts.main_shortcuts import filter_data, get_channel_as_text
from states.StatesGroup import ChannelState
from utils.db_api.manage import Channel


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('set_required'))
async def requirement_h(call: CallbackQuery):
    data = filter_data(call.data, 'set_required')
    status, channel_id = data.split('+')
    try:
        Channel(call.from_user.id).set_required(status, channel_id)
        await call.answer('Успешно!')
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                    text=get_channel_as_text(channel_id),
                                    reply_markup=await AdminButton().manage_channel(channel_id))

    except:
        await call.answer('Не получилось внесить изменения!')


@dp.message_handler(Text(contains='Каналы'))
async def channels_h(msg: Message):
    channels = Channel(msg.from_user.id).list()
    count = 1
    if channels == []:
        await msg.answer('Пусто', reply_markup=button('Добавить', '', 'add-channel'))
        return
    for channel in channels:
        text = (f'{count}.{channel[2]}.\n'
                f'Порядковый номер: {channel[0]}')
        await msg.answer(text, reply_markup=await AdminButton().manage_channel(channel[0]))


@dp.callback_query_handler(text='add-channel')
async def add_channel(call: CallbackQuery, state: FSMContext):
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                text='Название канала: \n'
                                     'Отменить: /break')
    await state.update_data(message_id=call.message.message_id)
    await state.set_state(ChannelState.get_title.state)


@dp.message_handler(state=ChannelState.get_title.state)
async def get_title(msg: Message, state: FSMContext):
    message_id = (await state.get_data()).get('message_id')
    await bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message_id)
    if 'break' in msg.text:
        await state.finish()
        await bot.delete_message(chat_id=msg.from_user.id, message_id=message_id)
        return
    await state.update_data(title=msg.text)
    await state.set_state(ChannelState.get_id.state)
    await bot.edit_message_text(chat_id=msg.from_user.id, message_id=message_id,
                                text='Введите идентификатор канала: \n'
                                     'Отменить: /break')


@dp.message_handler(state=ChannelState.get_id.state)
async def get_id_h(msg: Message, state: FSMContext):
    message_id = (await state.get_data()).get('message_id')
    await bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message_id)
    if 'break' in msg.text:
        await state.finish()
        await bot.delete_message(chat_id=msg.from_user.id, message_id=message_id)
        return
    data = await state.get_data()
    name = data.get('title')
    id = int(msg.text)
    try:
        await bot.get_chat(chat_id=id)
    except:
        await msg.answer('Возникла ошибка\n'
                         'Возможно ошибка в идентификаторе канала,\n'
                         'Либо вы не добавили бота в этот канал')
        await state.finish()
    try:
        Channel(msg.from_user.id).create(channel_id=id, name=name, is_required=0)
        await bot.edit_message_text(chat_id=msg.from_user.id, message_id=message_id, text='Канал добавлен!')
        await state.finish()
    except:
        await msg.answer('Ошибка!')


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('delete-channel'))
async def delete_channel_h(call: CallbackQuery):
    channel_id = filter_data(call.data, 'delete-channel')
    try:
        Channel(call.from_user.id).remove(channel_id)
        await call.answer('Удалено!')
    except:
        await call.answer('Не удалось удалить !', show_alert=True)
        return
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

