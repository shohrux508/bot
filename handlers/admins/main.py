from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

from keyboards.default.main import StartKeyboard
from keyboards.inline.admin import AdminButton
from keyboards.one_time_keyboards import button
from loader import dp, bot
from shortcuts.main_shortcuts import filter_data, get_users_as_text, manage_user_kb
from states.StatesGroup import Chat
from utils.db_api.manage import ManageUser, search_user, SubUserManager


@dp.message_handler(Text(contains='Отправить сообщение'))
async def send_message(msg: Message):
    if not ManageUser(msg.from_user.id).is_admin():
        return
    await msg.answer('Выберите: ', reply_markup=AdminButton().send_message_kb())


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('message_filter_by'))
async def answer(call: CallbackQuery, state: FSMContext):
    data = filter_data(call.data, 'message_filter_by=')
    keyboard = None
    language = ManageUser(call.from_user.id).language()
    if data == 'faculty':
        keyboard = AdminButton().send_message_by_faculty(language)
    elif data == 'direction':
        keyboard = AdminButton().direction_kbs()
    else:
        await state.set_state(Chat.get_public_msg.state)
        await bot.send_message(chat_id=call.from_user.id, text='Напишите текст сообщения!\n'
                                                               'Отменить: /break')

    if keyboard:
        await bot.send_message(chat_id=call.from_user.id, text='Выберите: ', reply_markup=keyboard)


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('send_message_by'))
async def answer(call: CallbackQuery, state: FSMContext):
    context = (filter_data(call.data, 'send_message_by_')).split("=")
    data = context[0]
    sub_data = context[1]
    list = SubUserManager(call.from_user.id).get(by=True, table_name=data, data=sub_data)
    id_list = []
    for i in list:
        id = i[4]
        id_list.append(id)

    await state.update_data(list=id_list)
    await state.set_state(Chat.get_public_msg.state)
    await bot.send_message(chat_id=call.from_user.id, text='Напишите текст сообщения!\n'
                                                           'Отменить: /break')


@dp.message_handler(state=Chat.get_public_msg.state)
async def get_public_msg_h(msg: Message, state: FSMContext):
    if 'break' in msg.text:
        await state.finish()
        await msg.answer('Отменено')
        return
    data = (await state.get_data()).get('list')
    if data:
        users = data
    else:
        users = ManageUser(msg.from_user.id).list(select_id=True, filter_by='', period=False)
    count = 0
    first_message_id = 0
    for id in users:
        if ManageUser(id).language() == 'uz':
            message = await bot.send_message(chat_id=id, text=msg.text)
        else:
            message = await bot.send_message(chat_id=id, text=msg.text)
        if count == 0:
            first_message_id = message.message_id

        count = count + 1
    await msg.answer(f'Отправлено({count}-пользователям)',
                     reply_markup=AdminButton().manage_sent_messages(message_id=first_message_id, count=count))
    await msg.answer('Главное', reply_markup=StartKeyboard(msg.from_user.id).keyboard())
    await state.finish()


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('send_message_to_user'))
async def send_message_(call: CallbackQuery, state: FSMContext):
    user_id = filter_data(call.data, 'send_message_to_user')
    await state.update_data(user_id=user_id, message_id=call.message.message_id)
    await state.set_state(Chat.get_private_msg_to_user.state)
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                text='Введите сообщение: \n'
                                     'Отменить: /break')
    await call.answer(f'Сообщение пользователю: {user_id}')


@dp.message_handler(state=Chat.get_private_msg_to_user.state)
async def answer(msg: Message, state: FSMContext):
    user_id = (await state.get_data()).get('user_id')
    message_id = (await state.get_data()).get('message_id')
    if 'break' in msg.text:
        await state.finish()
        await bot.delete_message(chat_id=msg.from_user.id, message_id=message_id)
        return
    if ManageUser(user_id).language() == 'uz':
        btn = 'Javob berish'
    else:
        btn = 'Ответить'
    try:
        message = await bot.send_message(chat_id=user_id, text=msg.text,
                                         reply_markup=button(btn, f'{msg.from_user.id}+{msg.message_id}', 'answer'))
        await bot.edit_message_text(chat_id=msg.from_user.id, message_id=message_id,
                                    text=f'Отправлено пользователю: {user_id}\n'
                                         f'Сообщение: {msg.text}',
                                    reply_markup=AdminButton().manage_sent_message(user_id=user_id,
                                                                                   message_id=message.message_id))
        await bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message_id)
    except:
        await msg.answer('Не удалось отправить сообщение!')

    await state.finish()


@dp.message_handler(Text(contains='Пользователи'))
async def users(msg: Message):
    if not ManageUser(msg.from_user.id).is_admin():
        return
    message = get_users_as_text(sort_by=False, filter_by=False, page=1, paginate_by=5)
    await msg.answer(message,
                     reply_markup=AdminButton().manage_users_list(sort_by=False, filter_by=False, page=1,
                                                                  paginate_by=5))


@dp.callback_query_handler(lambda x: x.data and x.data.startswith("prev-page"))
async def answer(call: CallbackQuery):
    datas = (filter_data(call.data, function='prev-page')).split("+")
    sort_by = datas[0]
    filter_by = datas[1]
    paginate_by = int(datas[3])
    page = int(datas[2])
    if page > 1:
        page = page - 1
    else:
        await call.answer('Первая страница!')

    text = get_users_as_text(sort_by, filter_by, page, paginate_by)
    try:
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text,
                                    reply_markup=AdminButton().manage_users_list(sort_by, filter_by, page, paginate_by))
    except:
        await call.answer('Ошибка!')


@dp.callback_query_handler(lambda x: x.data and x.data.startswith("next-page"))
async def answer(call: CallbackQuery):
    datas = (filter_data(call.data, function='next-page')).split("+")
    sort_by = datas[0]
    filter_by = datas[1]
    paginate_by = int(datas[3])
    page = int(datas[2]) + 1
    try:
        text = get_users_as_text(sort_by, filter_by, page, paginate_by)
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text,
                                    reply_markup=AdminButton().manage_users_list(sort_by, filter_by, page, paginate_by))

    except:
        await call.answer('Последняя страница!')


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('refresh'))
async def answer(call: CallbackQuery):
    datas = (filter_data(call.data, function='refresh')).split("+")
    sort_by = datas[0]
    filter_by = datas[1]
    paginate_by = int(datas[2])
    page = int(datas[3])
    text = get_users_as_text(sort_by, filter_by, paginate_by, page)
    try:
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text,
                                    reply_markup=AdminButton().manage_users_list(sort_by, filter_by, page, paginate_by))
    except:
        await call.answer('Ошибка!')


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('filter-by-'))
async def filter_by(call: CallbackQuery):
    data = filter_data(call.data, 'filter-by-')
    text = get_users_as_text(sort_by=False, filter_by=data, page=1, paginate_by=5)
    try:
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text,
                                    reply_markup=AdminButton().manage_users_list(sort_by=False, filter_by=data, page=1,
                                                                                 paginate_by=5))
    except:
        await call.answer('Ошибка!')


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('search-user'))
async def search_user_h1(call: CallbackQuery, state: FSMContext):
    await bot.send_message(chat_id=call.from_user.id, text='Введите номер телефона или Telegram ID: \n'
                                                           'Отменить: /break')
    await state.set_state(Chat.get_id_to_search.state)


@dp.message_handler(state=Chat.get_id_to_search.state)
async def search_user_h(msg: Message, state: FSMContext):
    if 'break' in msg.text:
        await state.finish()
        await msg.answer('отменено')
        return
    if search_user(msg.text) == False:
        await msg.answer('Пользователь не найден!')
    else:
        try:
            user_id, text = search_user(msg.text)
            await msg.answer(text, reply_markup=manage_user_kb(user_id, msg.from_user.id))
        except:
            await msg.answer('Ошибка при обработке данных!')
    await state.finish()

