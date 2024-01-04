from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message

from keyboards.inline.admin import AdminButton
from keyboards.one_time_keyboards import button
from loader import dp, bot
from shortcuts.main_shortcuts import filter_data, manage_user_kb
from states.StatesGroup import Chat
from utils.db_api.manage import ManageUser, search_user


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('answer'))
async def answer(call: CallbackQuery, state: FSMContext):
    data = filter_data(call.data, 'answer')
    user_id, message_id = data.split('+')
    if ManageUser(call.from_user.id).language() == 'uz':
        message = await bot.send_message(chat_id=call.from_user.id, text='Javobingizni yozing: \n'
                                                                         'Bekor qilish: /break')
    else:
        message = await bot.send_message(chat_id=call.from_user.id, text='Напишите текст: \n'
                                                                         'Отменить: /break')
    await state.update_data(user_id=user_id, message_id=message_id, msg_id=message.message_id)
    await state.set_state(Chat.get_message_to_answer.state)


@dp.message_handler(state=Chat.get_message_to_answer.state)
async def answer(msg: Message, state: FSMContext):
    msg_id = (await state.get_data()).get('msg_id')
    if 'break' in msg.text:
        await state.finish()
        await bot.delete_message(chat_id=msg.from_user.id, message_id=msg_id)
        return
    data = await state.get_data()
    user_id = data.get('user_id')
    message_id = data.get('message_id')
    try:
        if ManageUser(user_id).language() == 'uz':

            await bot.send_message(chat_id=user_id, text=msg.text, reply_to_message_id=message_id,
                                   reply_markup=button('Javob yozish', f'{msg.from_user.id}+{msg.message_id}',
                                                       'answer'))
        else:
            await bot.send_message(chat_id=user_id, text=msg.text, reply_to_message_id=message_id,
                                   reply_markup=button('Ответить', f'{msg.from_user.id}+{msg.message_id}', 'answer'))
    except:
        if ManageUser(msg.from_user.id).language() == 'uz':
            error_msg = ('Habarni yuborishda muammo yuzaga keldi.\n'
                         'Iltimos qaytadan urining!\n')
        else:
            error_msg = ('Не удалось отправить сообщение.\n'
                         'Попробуйте позже!')
        await msg.answer(error_msg)
        return
    await msg.answer('✅')
    await state.finish()


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('find_user'))
async def find_user(call: CallbackQuery):
    user_id = filter_data(call.data, 'find_user')
    if search_user(user_id) == False:
        await call.answer('Пользователь не найден!', show_alert=True)
    else:
        try:
            user_id, text = search_user(user_id)
            await bot.send_message(chat_id=call.from_user.id, text=text,
                                   reply_markup=manage_user_kb(user_id, call.from_user.id))
        except:
            await call.answer('Ошибка при обработке данных!', show_alert=True)


# edit
# 1

@dp.callback_query_handler(lambda x: x.data and x.data.startswith('edit-private-msg'))
async def edit_private_msg(call: CallbackQuery, state: FSMContext):
    data = filter_data(call.data, 'edit-private-msg')
    user_id, message_id = data.split("+")
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                text='Введите сообщение: \n'
                                     f'Сообщение будет изменено у пользователя: {user_id}\n'
                                     f'Отменить: /break')
    await state.update_data(user_id=user_id, message_id=message_id, msg_id=call.message.message_id)
    await state.set_state(Chat.edit_private_msg.state)


# 2
@dp.message_handler(state=Chat.edit_private_msg.state)
async def edit_private_msg(msg: Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get('user_id')
    message_id = data.get('message_id')
    msg_id = data.get('msg_id')
    try:
        await bot.edit_message_text(chat_id=user_id, message_id=message_id, text=msg.text,
                                    reply_markup=button('Ответить', f'{user_id}+{msg.message_id}', 'answer'))
        await bot.edit_message_text(chat_id=msg.from_user.id, message_id=msg_id, text='Успешно',
                                    reply_markup=AdminButton().manage_sent_message(user_id, message_id))
    except:
        await msg.answer('Не удалось изменить сообщение!\n'
                         'Возможно сообщение было удалено')


# delete message from private user
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('delete-private-msg'))
async def delete_private_msg(call: CallbackQuery):
    data = filter_data(call.data, 'delete-private-msg')
    user_id, message_id = data.split('+')
    await bot.delete_message(chat_id=user_id, message_id=message_id)
    await call.answer(f'Удалено у пользователя -> {user_id}', show_alert=True)


# delete messages from all users
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('delete-public-msgs'))
async def delete_sent_msgs(call: CallbackQuery):
    data = filter_data(call.data, 'delete-public-msgs')
    message_id, users_count = data.split('+')
    list = ManageUser(call.from_user.id).list(select_id=True, filter_by='', period=[0, users_count])
    try:
        for id in list:
            await bot.delete_message(chat_id=id, message_id=message_id)
            message_id = int(message_id) + 1
            await call.answer('Удалено!')
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        text='Удалено...')
    except:
        await call.answer('Не удалось удалить сообщения!', show_alert=True)


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('edit-public-msgs'))
async def edit_sent_msg_h(call: CallbackQuery, state: FSMContext):
    data = filter_data(call.data, 'edit-public-msgs')
    message_id, users_count = data.split('+')
    await state.update_data(message_id=message_id, users_count=users_count, msg_id=call.message.message_id)
    await state.set_state(Chat.edit_public_msgs.state)

    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                text='Отправьте новое сообщение: \n'
                                     'Отменить: /break')


@dp.message_handler(state=Chat.edit_public_msgs.state)
async def edit_public_msgs(msg: Message, state: FSMContext):
    msg_id = (await state.get_data()).get('msg_id')
    if 'break' in msg.text:
        await state.finish()
        await bot.delete_message(chat_id=msg.from_user.id, message_id=msg_id)
        return
    data = await state.get_data()
    message_id = data.get('message_id')
    users_count = data.get('users_count')
    list = ManageUser(msg.from_user.id).list(select_id=True, filter_by='', period=[0, users_count])
    try:
        for id in list:
            await bot.edit_message_text(chat_id=id, message_id=message_id, text=msg.text,
                                        reply_markup=button('Ответить', f'{msg.from_user.id}+{msg.message_id}', ''))
            message_id = int(message_id) + 1

        await bot.send_message(chat_id=msg.from_user.id, text='Публичиное сообщение изменено!\n'
                                                              f'Сообщение: {msg.text}',
                               reply_markup=AdminButton().manage_sent_messages(message_id, users_count))
    except:
        pass
    await state.finish()
