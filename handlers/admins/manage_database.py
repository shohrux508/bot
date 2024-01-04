import os
import time as t

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.inline.admin import AdminButton
from keyboards.one_time_keyboards import button
from loader import dp, bot
from shortcuts.main_shortcuts import filter_data, download_users_excel_file, manage_faculty_btns
from states.StatesGroup import FacultyState, DirectionState
from utils.db_api.manage import SubUserManager, ManageUser, FacultyManager, DirectionManager


# download excel document
@dp.message_handler(commands='get_users_as_excel')
async def answer(msg: Message):
    if not ManageUser(msg.from_user.id).is_admin():
        return
    await msg.answer('Выберите: ', reply_markup=AdminButton().download_users())


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('download'))
async def download(call: CallbackQuery):
    data = filter_data(call.data, 'download=')
    if data == 'participants':
        length = len(SubUserManager(call.from_user.id).list())
        file_path = f'data/excel/SubUsers{length}.xlsx'
    else:
        length = len(ManageUser(user_id='').list(select_id=False, filter_by=False, period=False))
        file_path = f'data/excel/Users{length}.xlsx'
    if os.path.exists(file_path):
        document = open(f'{file_path}', 'rb')
        await bot.send_document(chat_id=call.from_user.id, document=document, caption='Таблица пользователей')
        os.remove(file_path)
    else:
        message = await bot.send_message(chat_id=call.from_user.id, text='Подождите пока идёт обработка данных! ')
        download_users_excel_file(filter_by=data)

        for i in range(1, 10):
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=message.message_id,
                                        text=f'Подождите пока идёт обработка данных! {10 - i}')
            t.sleep(1)
        await bot.delete_message(chat_id=call.from_user.id, message_id=message.message_id)
        document = open(f'{file_path}', 'rb')
        await bot.send_document(chat_id=call.from_user.id, document=document, caption='Таблица пользователей')
        try:
            os.remove(file_path)
        except:
            pass


@dp.message_handler(commands='directions')
async def answer(msg: Message):
    await msg.answer('Языки программирования', reply_markup=AdminButton().manage_programming_languages())


@dp.callback_query_handler(text='programming-languages-list')
async def answer(call: CallbackQuery):
    list = DirectionManager().list(select_title=False)
    for i in list:
        await bot.send_message(chat_id=call.from_user.id, text=f'{i[1]}',
                               reply_markup=button('Удалить', f'{i[0]}', 'delete-direction'))


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('delete-direction'))
async def delete_dir(call: CallbackQuery):
    id = filter_data(call.data, 'delete-direction')
    DirectionManager().remove(id=id)
    await call.answer('Успешно удалено!')
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)


# add programming language
@dp.callback_query_handler(text='add-programming-language')
async def add_pro(call: CallbackQuery, state: FSMContext):
    if not ManageUser(call.from_user.id).is_admin():
        return
    message = await bot.send_message(chat_id=call.from_user.id, text=
    'Напишите название языка программирования или отправьте список(в списке используйте только запятые)\n'
    'Отменить: /break')
    await state.update_data(message_id=message.message_id)
    await state.set_state(DirectionState.get_titles.state)


@dp.message_handler(state=DirectionState.get_titles.state)
async def get_title(msg: Message, state: FSMContext):
    message_id = (await state.get_data()).get('message_id')
    if '/break' in msg.text:
        await state.finish()
        await bot.delete_message(chat_id=msg.from_user.id, message_id=message_id)
        return
    try:
        if ',' in msg.text:
            list = (msg.text).split(',')
            for i in list:
                DirectionManager().create(title=i)
        else:
            DirectionManager().create(title=msg.text)
        await bot.edit_message_text(chat_id=msg.from_user.id, message_id=message_id, text='Данные успешно сохранились!')
        await state.finish()
    except:
        await bot.edit_message_text(chat_id=msg.from_user.id, message_id=message_id,
                                    text='Возникла ошибка при сохранение данных!')
    await bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message_id)


@dp.message_handler(commands='faculties')
async def faculties(msg: Message):
    await msg.answer('Факультеты', reply_markup=AdminButton().manage_faculties())


@dp.callback_query_handler(text='faculties-list')
async def faculties_list(call: CallbackQuery):
    kb1, kb2 = AdminButton().faculties_kbs('delete-')
    await bot.send_message(chat_id=call.from_user.id, text='Факультеты на русском-языке:\n', reply_markup=kb1)
    await bot.send_message(chat_id=call.from_user.id, text='Факультеты на узбекском-языке:\n', reply_markup=kb2)
    t.sleep(1)
    await call.answer('Выберите для удаления!', show_alert=True)


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('delete-faculty'))
async def delete_fac(call: CallbackQuery):
    id = filter_data(call.data, 'delete-faculty=')
    language = (FacultyManager().get(id=id))[2]
    try:
        FacultyManager().remove(id=id)
    except:
        await call.answer('Не удалось удалить!')
        return
    await call.answer('Удалено!')
    await bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.message_id,
                                        reply_markup=manage_faculty_btns(language))


# add faculties
@dp.callback_query_handler(text='add-faculty')
async def add_fac(call: CallbackQuery, state: FSMContext):
    if not ManageUser(call.from_user.id).is_admin():
        return
    message = await bot.send_message(chat_id=call.from_user.id, text=
    'Напишите название факультета или отправьте список факультетов(в списке используйте только запятые)!')
    await state.update_data(message_id=message.message_id)
    await state.set_state(FacultyState.get_titles.state)


@dp.message_handler(state=FacultyState.get_titles.state)
async def get_fac(msg: Message, state: FSMContext):
    message_id = (await state.get_data()).get('message_id')
    if '/break' in msg.text:
        await state.finish()
        await bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message_id)
        await bot.delete_message(chat_id=msg.from_user.id, message_id=message_id)
        return
    if 'fakulteti' in msg.text or 'fakultet' in msg.text:
        language = 'uz'
    else:
        language = 'ru'
    if ',' in msg.text:
        context = (msg.text).split(',')
        for title in context:
            if '\n' in title:
                title = title.replace('\n', '')
            FacultyManager().create(title, language)
    else:
        context = msg.text
        FacultyManager().create(context, language)

    await bot.edit_message_text(chat_id=msg.from_user.id, message_id=message_id,
                                text='Данные сохранились можете проверить их командой /faculties !')
    await state.finish()
    await bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message_id)
