from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import CallbackQuery

from data.config import ADMINS
from keyboards.default.main import StartKeyboard, OneTimeKeyboards
from keyboards.inline.user import share_language
from loader import dp, bot
from shortcuts.main_shortcuts import filter_data
from states.StatesGroup import RegisterUser
from utils.db_api.manage import ManageUser


# нижe написан код для обработки данных с новый пользователей


# start


@dp.message_handler(CommandStart())
async def start_bot(message: types.Message, state: FSMContext):
    if ManageUser(message.from_user.id).is_user():
        if ManageUser(message.from_user.id).language() == 'ru':
            text = 'Здраствуйте'
        else:
            text = 'Assolomu alaykum'
        await message.answer(text, reply_markup=StartKeyboard(user_id=message.from_user.id).keyboard())

    else:
        if str(message.from_user.id) in ADMINS:
            await state.set_state(RegisterUser.get_phone.state)
            await message.answer('Поделитесь номером телефона',
                                 reply_markup=OneTimeKeyboards(message.from_user.id).share_phone())
            ManageUser(message.from_user.id).new(full_name=message.from_user.full_name, phone='None', is_admin=1,
                                                 is_blocked=0, language='ru')
            return
        else:
            ManageUser(message.from_user.id).new(full_name=message.from_user.full_name, phone='None', is_admin=0,
                                                 is_blocked=0, language='ru')
            await message.answer('Assolomu alaykum, Tilni tanlang!\n'
                                 'Здраствуйте, Выберите язык!', reply_markup=share_language(message.from_user.id))


# this handler sets language which will choose user, after sets state to get phone number

@dp.callback_query_handler(lambda x: x.data and x.data.startswith('set_language'))
async def set_language_h(call: CallbackQuery, state: FSMContext):
    user_id, language = (filter_data(call.data, 'set_language')).split('+')
    ManageUser(call.from_user.id).set_language(language)
    if ManageUser(user_id).is_user():
        await call.answer('✅')
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)

    if language == 'ru':
        await bot.send_message(chat_id=call.from_user.id, text='Введите номер телефона!',
                               reply_markup=OneTimeKeyboards(user_id).share_phone())
        await call.answer('Вы выбрали русский язык')
    else:
        await bot.send_message(chat_id=call.from_user.id, text='Telefon raqamingizni kiriting!',
                               reply_markup=OneTimeKeyboards(call.from_user.id).share_phone())
        await call.answer("Siz o'zbek tilini tanladingiz")

    await state.set_state(RegisterUser.get_phone.state)

    # await call.answer('Не удалось применить язык,\n'
    #                   'Пожалуйста попробуйте перезапустить бот!')


# this handler gets phone number and updates user data -> set phone
@dp.message_handler(state=RegisterUser.get_phone.state, content_types=['contact', 'number'])
async def register_user(msg: types.Message, state: FSMContext):
    if msg.content_type == 'contact':
        phone = msg.contact.phone_number
    else:
        phone = msg.text
    ManageUser(msg.from_user.id).set_phone(phone=phone)
    if ManageUser(msg.from_user.id).is_admin():
        await msg.answer('Добро пожаловать', reply_markup=StartKeyboard(msg.from_user.id).keyboard())
        return

    if ManageUser(msg.from_user.id).language() == 'ru':
        await msg.answer('Добро пожаловать!\n', reply_markup=StartKeyboard(user_id=msg.from_user.id).keyboard())
        await msg.answer('Команды: \n'
                         '/change_language -> смена языка\n'
                         '/register -> зарегистрироваться'
                         '/help -> помощь\n'
                         '/')
    else:
        await msg.answer('Xush kelibsiz!\n', reply_markup=StartKeyboard(user_id=msg.from_user.id).keyboard())
        await msg.answer('Buyruqlar: \n'
                         '/change_language -> tilni o\'zgartirish \n'
                         '/register -> ro\'yxatdan o\'tish'
                         '/help -> yordam \n'
                         '/')
    await state.finish()
