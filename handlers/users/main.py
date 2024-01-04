from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards.default.main import StartKeyboard
from keyboards.inline.user import share_language
from keyboards.one_time_keyboards import button
from loader import dp, bot
from shortcuts.main_shortcuts import check_is_member
from states.StatesGroup import Registration_uz, Registration_ru
from utils.db_api.manage import ManageUser, SubUserManager


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('check_subscription'))
async def check(call: CallbackQuery):
    await check_is_member(call.from_user.id)


@dp.message_handler(commands='register')
async def register_h(msg: Message, state: FSMContext):
    user = SubUserManager(msg.from_user.id).is_registered()
    if ManageUser(msg.from_user.id).language() == 'ru':
        if user:
            await msg.answer('Вы уже зарегистрировались!', reply_markup=button('Проверить', '', 'check.get_datas'))
            return
        sub_msg = await msg.answer('Как вас зовут?'
                                   '\nОтменить: /break')
        await state.set_state(Registration_ru.get_full_name.state)
    else:
        if user:
            await msg.answer("Siz avval ro'yxatdan o'tgansiz!",
                             reply_markup=button('Tekshirish📃', '', 'check.get_datas'))
            return
        sub_msg = await msg.answer('Ismingizni kiriting: \n'
                                   '\nBekor qilish: /break')
        await state.set_state(Registration_uz.get_full_name.state)
    await state.update_data(message_id=sub_msg.message_id)


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('check.get_datas'))
async def check_dt(call: CallbackQuery):
    user = (SubUserManager(call.from_user.id).get(by=False, table_name='', data=''))

    if ManageUser(call.from_user.id).language() == 'uz':
        text = (f'F.I.O: {user[0]}\n'
                f'ID raqamingiz: {user[6]}\n'
                f'Fakultet: {user[1]}\n'
                f'Guruhingiz: {user[2]}\n'
                f'Dasturlash tili: {user[3]}\n'
                f"Ro'yxatdan o'tilgan sana: {user[5]}\n")

        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text,
                                    reply_markup=button("Ma'lumotlarni tahrirlash📝", '', 'check.edit_datas'))

    else:
        text = (f'ФИО: {user[0]}\n'
                f'Порядковый номер: {user[6]}'
                f'Факультет: {user[1]}\n'
                f'Группа: {user[2]}\n'
                f'Специальность: {user[3]}\n'
                f'Дата регистратции: {user[5]}\n')

        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=text,
                                    reply_markup=button('Изменить данные📝', '', 'check.edit_datas'))


@dp.callback_query_handler(text='check.edit_datas')
async def edit_dt(call: CallbackQuery, state: FSMContext):
    user = SubUserManager(call.from_user.id).get(by=False, table_name='', data='')
    await state.update_data(is_edited=True, id=user[6])
    await state.update_data(message_id=call.message.message_id)
    if ManageUser(call.from_user.id).language() == 'uz':
        await state.set_state(Registration_uz.get_full_name.state)

        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                    text="Ismingizni kiriting: \n"
                                         "Bekor qilish: /break\n")
    else:
        await state.set_state(Registration_ru.get_full_name.state)
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                    text="Как вас зовут? \n"
                                         "Отменить: /break")


@dp.callback_query_handler(text='register')
async def register(call: CallbackQuery, state: FSMContext):
    user = SubUserManager(call.from_user.id).is_registered()
    if ManageUser(call.from_user.id).language() == 'ru':
        if user:
            await bot.send_message(chat_id=call.from_user.id, text='Вы уже зарегистрировались!',
                                   reply_markup=button('Проверить', '', 'check.get_datas'))
            return
        sub_msg = await bot.send_message(chat_id=call.from_user.id, text='Как вас зовут?'
                                                                         '\nОтменить: /break')
        await state.set_state(Registration_ru.get_full_name.state)
    else:
        if user:
            await bot.send_message(chat_id=call.from_user.id, text="Siz avval ro'yxatdan o'tgansiz!",
                                   reply_markup=button('Tekshirish📃', '', 'check.get_datas'))
            return
        sub_msg = await bot.send_message(chat_id=call.from_user.id, text='Ismingizni kiriting: \n'
                                                                         '\nBekor qilish: /break')
        await state.set_state(Registration_uz.get_full_name.state)
    await state.update_data(message_id=sub_msg.message_id)


@dp.message_handler(commands='change_language')
async def answer(msg: Message):
    await bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message_id)
    await msg.answer('Выберите: \nTanlang: ', reply_markup=share_language(msg.from_user.id))


@dp.callback_query_handler(text='main')
async def answer(call: CallbackQuery):
    if ManageUser(call.from_user.id).language() == 'uz':
        await bot.send_message(chat_id=call.from_user.id, text='Asosiy',
                               reply_markup=StartKeyboard(call.from_user.id).keyboard())
    else:
        await bot.send_message(chat_id=call.from_user.id, text='Главное',
                               reply_markup=StartKeyboard(call.from_user.id).keyboard())

