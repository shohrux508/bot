from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

from keyboards.default.main import OneTimeKeyboards
from keyboards.inline.admin import AdminButton
from keyboards.inline.user import faculty_kbs, programming_languages_kbs, finish_registration_kb
from keyboards.one_time_keyboards import button, url_button
from loader import dp, bot
from states.StatesGroup import Registration_ru, Chat, ExamplesState
from utils.db_api.manage import SubUserManager, FacultyManager, ManageUser, ExamplesManager


@dp.message_handler(Text(contains='Олимпиада'))
async def answer(msg: Message):
    await msg.answer('Зарегестрируйтесь на Олимпиады', reply_markup=button('Зарегистрироваться', '', 'register'))


@dp.message_handler(Text(contains='Обратная связь'))
async def answer(msg: Message):
    await bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message_id)
    await msg.answer('Ваше сообщение будет отравлено администраторам!: ',
                     reply_markup=button('Отправить сообщение✅', '', 'msg_to_admin_ru'))


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('msg_to_admin_ru'))
async def msg_to_admin(call: CallbackQuery, state: FSMContext):
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                text='Напишите текст сообщение: \n'
                                     'Отменить /break')
    await state.update_data(message_id=call.message.message_id)
    await state.set_state(Chat.get_private_msg_to_admin.state)


@dp.message_handler(state=Chat.get_private_msg_to_admin.state)
async def send_Message_to_admin(msg: Message, state: FSMContext):
    message_id = (await state.get_data()).get('message_id')
    if msg.text.startswith('/break'):
        await bot.edit_message_text(chat_id=msg.from_user.id, message_id=message_id, text='Отменено!')
    else:
        list = ManageUser(msg.from_user.id).list(select_id=True, filter_by='admin', period=False)
        for id in list:
            await bot.send_message(chat_id=id, text=msg.text,
                                   reply_markup=button('Ответить', f'{msg.from_user.id}+{msg.message_id}', 'answer'))
        await bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message_id)
        await bot.edit_message_text(chat_id=msg.from_user.id, message_id=message_id, text='Сообщение отправлено!\n'
                                                                                          f'Сообщение: {msg.text}',
                                    reply_markup=button("Новое сообщение", '', 'msg_to_admin_ru'))
    await state.finish()


@dp.message_handler(Text(contains='Рекомендации по улучшению бота'))
async def answer(msg: Message):
    await msg.answer('У вас есть советы или жалобы?\n'
                     'Напишите нам и мы вам ответим! ', reply_markup=button('Написать', '', 'msg_to_admin_ru'))


@dp.message_handler(Text(contains='Видеоуроки'))
async def answer(msg: Message):
    await msg.answer('Видеоуроки', reply_markup=url_button('Перейти', url='https://t.me/Video_darsliklar_bot'))
    await bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message_id)


@dp.message_handler(state=Registration_ru.get_full_name.state)
async def answer(msg: Message, state: FSMContext):
    message_id = (await state.get_data()).get('message_id')
    try:
        await bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message_id)
    except:
        pass
    if '/break' in (msg.text).lower():
        await bot.edit_message_text(chat_id=msg.from_user.id, message_id=message_id, text='Отменено!')
        await state.finish()
    else:
        await state.update_data(full_name=msg.text)
        await state.set_state(Registration_ru.get_faculty.state)
        await bot.edit_message_text(chat_id=msg.from_user.id, message_id=message_id,
                                    text='Выберите факультет: ',
                                    reply_markup=faculty_kbs(language='ru'))


@dp.callback_query_handler(state=Registration_ru.get_faculty.state)
async def get_faculty(call: CallbackQuery, state: FSMContext):
    message_id = (await state.get_data()).get('message_id')
    if 'break' in call.data:
        await state.finish()
        try:
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=message_id, text='Отменено!')
        except:
            pass
        return
    id, language = (call.data).split("+")
    title = (FacultyManager().get(id))[1]
    await state.update_data(faculty=title)
    await call.answer('Сохранено!')
    try:
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=message_id, text='Введите вашу группу!\n'
                                                                                           'Образец: 152-23\n'
                                                                                           '\nОтмена: /break')
    except:
        pass
    await state.set_state(Registration_ru.get_group_name.state)


@dp.message_handler(state=Registration_ru.get_group_name.state)
async def get_group_name(msg: Message, state: FSMContext):
    message_id = (await state.get_data()).get('message_id')
    try:
        await bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message_id)
    except:
        pass
    if '/break' in (msg.text).lower():
        await state.finish()
        await bot.edit_message_text(chat_id=msg.from_user.id, message_id=message_id, text='Отменено!')
        return

    await state.update_data(group_name=msg.text)
    try:
        await bot.edit_message_text(chat_id=msg.from_user.id, message_id=message_id,
                                    text='Какой язык программирования вы знаете?',
                                    reply_markup=programming_languages_kbs(user_id=msg.from_user.id))
    except:
        pass
        await state.finish()

    await state.set_state(Registration_ru.get_programming_language.state)


@dp.callback_query_handler(state=Registration_ru.get_programming_language.state)
async def get_programming_language(call: CallbackQuery, state: FSMContext):
    message_id = (await state.get_data()).get('message_id')
    if 'break' in call.data:
        await state.finish()
        try:
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=message_id, text='Отменено!')
        except:
            pass
        return
    programming_language = call.data
    data = await state.get_data()
    full_name = data.get('full_name')
    faculty = data.get('faculty')
    group = data.get('group_name')
    text = (f'Ваши данные: \n'
            f'Ф.И.О: {full_name}\n'
            f'Факультет: {faculty}\n'
            f'Группа: {group}\n'
            f'Язык программирования: {programming_language}')
    await state.update_data(programming_language=programming_language)
    try:
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=message_id, text=text,
                                    reply_markup=finish_registration_kb(language='ru'))
    except:
        pass
        await state.finish()
    await state.set_state(Registration_ru.finish.state)


@dp.callback_query_handler(state=Registration_ru.finish.state)
async def finish_registration(call: CallbackQuery, state: FSMContext):
    is_update = (await state.get_data()).get('is_edited')
    id = None
    message_id = (await state.get_data()).get('message_id')
    if 'break' in call.data:
        await state.finish()
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=message_id, text='Отменено!')
        return
    messageText = False
    if call.data == 'submit':
        data = await state.get_data()
        full_name = data.get('full_name')
        faculty = data.get('faculty')
        group = data.get('group_name')
        programming_language = data.get('programming_language')
        try:
            if is_update:
                id = (await state.get_data()).get('id')
                SubUserManager(user_id=call.from_user.id).update(full_name, faculty, group, programming_language, id)
            else:
                id = SubUserManager(call.from_user.id).create(full_name, faculty, group, programming_language)
        except:
            await call.answer(
                'Не удалось сохранить ваши данные, пожалуйста повторите попытку либо свяжитесь а администратором!')
            return
        await call.answer("Данные успешно сохранены!")
        messageText = "Данные успешно сохранены!\n" \
                      f"Ваш порядковый номер: {id}"
    elif call.data == 'retry':
        await state.reset_data()
        await state.set_state(Registration_ru.get_full_name.state)
        sub_msg = await bot.send_message(chat_id=call.from_user.id, text='Как вас зовут?: ',
                                         reply_markup=OneTimeKeyboards(call.from_user.id).share_phone())
        await state.update_data(message_id=sub_msg)
        return
    await state.finish()
    if not messageText:
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        return
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=messageText)
    await bot.pin_chat_message(chat_id=call.from_user.id, message_id=call.message.message_id)


@dp.message_handler(Text(contains='Образцы для подготовки'))
async def examples(msg: Message, state: FSMContext):
    message = await msg.answer('Выберите: ', reply_markup=AdminButton().direction_kbs())
    await state.update_data(message_id=message.message_id)
    await state.set_state(ExamplesState.get_programming_language.state)


@dp.callback_query_handler(state=ExamplesState.get_programming_language.state)
async def answer(call: CallbackQuery, state: FSMContext):
    message_id = (await state.get_data()).get('message_id')
    await bot.delete_message(chat_id=call.from_user.id, message_id=message_id)
    if 'break' in call.data or call.message.message_id != message_id:
        await state.finish()
        await call.answer('Отменено!')
        return
    list = ExamplesManager().list(programming_language=call.data.lower())
    if list == []:
        await call.answer('Данные отсутствуют!')
        await state.finish()
        return
    for i in list:
        await bot.send_document(chat_id=call.from_user.id, document=i[3])
    await state.finish()
