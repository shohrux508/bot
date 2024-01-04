from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

from keyboards.default.main import StartKeyboard, OneTimeKeyboards
from keyboards.inline.admin import AdminButton
from keyboards.inline.user import faculty_kbs, programming_languages_kbs, finish_registration_kb
from keyboards.one_time_keyboards import button, url_button
from loader import dp, bot
from states.StatesGroup import Registration_uz, ChatUz, ExamplesState
from utils.db_api.manage import ManageUser, SubUserManager, FacultyManager, ExamplesManager



# registration -> start

@dp.message_handler(state=Registration_uz.get_full_name.state)
async def answer(msg: Message, state: FSMContext):
    message_id = (await state.get_data()).get('message_id')
    try:
        await bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message_id)
    except:
        pass
    if '/break' in (msg.text).lower():
        await bot.edit_message_text(chat_id=msg.from_user.id, message_id=message_id, text='Bekor qilindi!')
        await state.finish()
        await bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message_id)
    else:
        await state.update_data(full_name=msg.text)
        await state.set_state(Registration_uz.get_faculty.state)

        await bot.edit_message_text(chat_id=msg.from_user.id, message_id=message_id, text='Fakultetingizni tanlang!',
                                    reply_markup=faculty_kbs(language='uz'))


@dp.callback_query_handler(state=Registration_uz.get_faculty.state)
async def get_faculty(call: CallbackQuery, state: FSMContext):
    message_id = (await state.get_data()).get('message_id')
    if 'break' in call.data:
        await state.finish()
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=message_id, text='Bekor qilindi!')
        return
    id, language = (call.data).split("+")
    title = (FacultyManager().get(id))[1]
    await state.update_data(faculty=title)
    await call.answer('Saqlandi')
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=message_id, text='Guruhingizni kiriting!\т'
                                                                                       'Misol uchung: 152-23'
                                                                                       '\nBekor qilish: /break')

    await state.set_state(Registration_uz.get_group_name.state)


@dp.message_handler(state=Registration_uz.get_group_name.state)
async def get_group_name(msg: Message, state: FSMContext):
    message_id = (await state.get_data()).get('message_id')

    await bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message_id)
    if '/break' in (msg.text).lower():
        await state.finish()
        await bot.edit_message_text(chat_id=msg.from_user.id, message_id=message_id, text='Bekor qilindi')
    else:

        await state.update_data(group_name=msg.text)
        await bot.edit_message_text(chat_id=msg.from_user.id, message_id=message_id,
                                    text='Qaysi dasturlash tilini bilasiz?',
                                    reply_markup=programming_languages_kbs(user_id=msg.from_user.id))

        await state.set_state(Registration_uz.get_programming_language.state)


@dp.callback_query_handler(state=Registration_uz.get_programming_language.state)
async def get_programming_language(call: CallbackQuery, state: FSMContext):
    message_id = (await state.get_data()).get('message_id')
    if 'break' in call.data:
        await state.finish()
        try:
            await bot.edit_message_text(chat_id=call.from_user.id, message_id=message_id, text='Bekor qilindi!')
        except:
            pass
        return
    programming_language = call.data
    data = await state.get_data()
    full_name = data.get('full_name')
    faculty = data.get('faculty')
    group = data.get('group_name')
    text = (f'Sizning Ma\'lumotlaringiz: \n'
            f'F.I.SH: {full_name}\n'
            f'Fakultet: {faculty}\n'
            f'Guruh: {group}\n'
            f'Dasturlash tili: {programming_language}')
    await state.update_data(programming_language=programming_language)
    try:
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=message_id, text=text,
                                    reply_markup=finish_registration_kb(language='uz'))
    except:
        await bot.send_message("Hatolik yuzaga keldi iltimos qaytadan urinib ko'ring!\n"
                               "/register")
        await state.finish()
    await state.set_state(Registration_uz.finish.state)


@dp.callback_query_handler(state=Registration_uz.finish.state)
async def finish_registration(call: CallbackQuery, state: FSMContext):
    is_update = (await state.get_data()).get('is_edited')
    message_id = (await state.get_data()).get('message_id')
    if 'break' in call.data:
        await state.finish()
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=message_id, text='Bekor qilindi!')
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
            await call.answer('Saqlashda hatolik yuzaga keldi!')
            return
        await call.answer("Ma'lumotlar muvaffaqiyatli saqlandi!")
        messageText = "Ma'lumotlar muvaffaqiyatli saqlandi!\n" \
                      f"Sizning id raqamingiz: {id}"
    elif call.data == 'retry':
        await state.reset_data()
        await state.set_state(Registration_uz.get_full_name.state)
        sub_msg = await bot.send_message(chat_id=call.from_user.id, text='Ismingizni kiriting: ',
                                         reply_markup=OneTimeKeyboards(call.from_user.id).share_phone())
        await state.update_data(message_id=sub_msg)
        return
    await state.finish()
    if not messageText:
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        return
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=messageText)
    pin_msg = await bot.pin_chat_message(chat_id=call.from_user.id, message_id=call.message.message_id)


# register -> end

@dp.message_handler(Text(contains='Olimpiada'))
async def answer(msg: Message):
    await msg.answer('Olimpiada: ', reply_markup=button("Ro'yxatdan o'tish", '', 'register'))


@dp.message_handler(Text(contains='Qayta aloqa'))
async def answer(msg: Message):
    await bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message_id)
    await msg.answer("Sizning habaringiz administratorlarga yuboriladi va 24 soat ichida habaringizga jabov olasiz: ",
                     reply_markup=button("Habar yuborish ✅", "", "msg_to_admin_uz"))


@dp.callback_query_handler(lambda x: x.data and x.data.startswith("msg_to_admin_uz"))
async def send_msg_to_admin(call: CallbackQuery, state: FSMContext):
    await state.update_data(message_id=call.message.message_id)
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                text='Habarni kiriting: \n'
                                     'Bekor qilish: /break')
    await call.answer('Qayta aloqa!')
    await state.set_state(ChatUz.get_private_msg_to_admin.state)


@dp.message_handler(state=ChatUz.get_private_msg_to_admin.state)
async def answer(msg: Message, state: FSMContext):
    message_id = (await state.get_data()).get("message_id")
    if msg.text.startswith('/break'):
        await bot.edit_message_text(chat_id=msg.from_user.id, message_id=message_id, text='Bekor qilindi!')
    else:
        list = ManageUser(msg.from_user.id).list(select_id=True, filter_by='admin', period=False)
        for id in list:
            await bot.send_message(chat_id=id, text=msg.text,
                                   reply_markup=button('Ответить', f'{msg.from_user.id}+{msg.message_id}', 'answer'))
        await bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message_id)
        await bot.edit_message_text(chat_id=msg.from_user.id, message_id=message_id, text='Habar yuborildi!\n'
                                                                                          f'Sizning habaringiz: {msg.text}',
                                    reply_markup=button("Yangi habar", '', 'msg_to_admin_uz'))
    await state.finish()


@dp.message_handler(Text(contains='Tayyorlanish uchun'))
async def examples(msg: Message, state: FSMContext):
    message = await msg.answer('Tanlang: ', reply_markup=AdminButton().direction_kbs())
    await state.update_data(message_id=message.message_id)
    await state.set_state(ExamplesState.get_programming_language_uz.state)


@dp.callback_query_handler(state=ExamplesState.get_programming_language_uz.state)
async def answer(call: CallbackQuery, state: FSMContext):
    message_id = (await state.get_data()).get('message_id')
    await bot.delete_message(chat_id=call.from_user.id, message_id=message_id)
    if 'break' in call.data or call.message.message_id != message_id:
        await state.finish()
        await call.answer('Bekor qilindi!')
        return
    list = ExamplesManager().list(programming_language=call.data.lower())
    if list == []:
        await call.answer("Ma'lumotlar topilmadi!")
        await state.finish()
        return
    for i in list:
        await bot.send_document(chat_id=call.from_user.id, document=i[3])
    await state.finish()


@dp.message_handler(Text(contains='Taklif'))
async def answer(msg: Message, state: FSMContext):
    message = await msg.answer('Habarni kiriting: \n'
                               'bekor qilish: /break')
    await state.update_data(message_id=message.message_id)
    await state.set_state(ChatUz.get_private_msg_to_admin.state)


@dp.message_handler(Text(contains='Videodarslar'))
async def answer(msg: Message):
    await msg.answer('Videodarslar', reply_markup=url_button('Botga o\'tish ', url='https://t.me/Video_darsliklar_bot'))
    await msg.delete()
