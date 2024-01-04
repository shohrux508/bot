from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards.inline.admin import AdminButton
from loader import dp, bot
from shortcuts.main_shortcuts import filter_data
from states.StatesGroup import ExamplesState, Chat
from utils.db_api.manage import ManageUser, ExamplesManager


@dp.message_handler(commands='examples')
async def examples(msg: Message):
    if ManageUser(msg.from_user.id).is_admin():
        await msg.answer('Образцы', reply_markup=AdminButton().manage_examples())
        await msg.delete()


@dp.callback_query_handler(text='see-list')
async def answer(call: CallbackQuery, state: FSMContext):
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text='Выберите: ',
                                reply_markup=AdminButton().direction_kbs())
    await state.set_state(ExamplesState.see_list.state)


@dp.callback_query_handler(state=ExamplesState.see_list.state)
async def see_list(call: CallbackQuery, state: FSMContext):
    if call.data == 'break':
        await state.finish()
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        return
    if AdminButton().examples_kbs(programming_language=call.data.lower()) == False:
        await call.answer('Данные отсутствуют!')
        await state.finish()
        return
    print(call.data.lower())
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text='Выберите: ',
                                reply_markup=AdminButton().examples_kbs(programming_language=call.data.lower()))
    await state.finish()


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('example'))
async def example(call: CallbackQuery):
    id = filter_data(call.data, 'example=')
    example = ExamplesManager().get(id=id)
    if example is None:
        await call.answer('Данные отсутствуют!')
        return
    try:
        await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=f'{example[1]}',
                                    reply_markup=AdminButton().manage_example_single(id=id))
    except:
        await call.answer('Возникла ошибка!')


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('delete-example'))
async def delete(call: CallbackQuery):
    id = filter_data(call.data, 'delete-example=')
    try:
        ExamplesManager().remove(id)
    except:
        await call.answer('Не удалось удалить!', show_alert=True)
        return
    await call.answer('Успешно')
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('see-example'))
async def see(call: CallbackQuery):
    id = filter_data(call.data, 'see-example=')
    example = ExamplesManager().get(id=id)
    try:
        await bot.send_document(chat_id=call.from_user.id, document=example[3], caption=example[1])
    except:
        await call.answer('Возникла ошибка!')
        return
    await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('add-example'))
async def add_example(call: CallbackQuery, state: FSMContext):
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text='Выберите: \n',
                                reply_markup=AdminButton().direction_kbs())
    await state.update_data(message_id=call.message.message_id)
    await state.set_state(Chat.add_example1.state)


@dp.callback_query_handler(state=Chat.add_example1.state)
async def answer(call: CallbackQuery, state: FSMContext):
    if 'break' in call.data:
        await state.finish()
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        return
    await state.update_data(programming_language=call.data.lower())
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                text='Отправьте PDF файл: \n'
                                     'Отменить: /break')
    await state.set_state(Chat.add_example2.state)


@dp.message_handler(state=Chat.add_example2.state, content_types=['document', 'text'])
async def answer(msg: Message, state: FSMContext):
    message_id = (await state.get_data()).get('message_id')
    if msg.text:
        if 'break' in msg.text:
            await state.finish()
            await bot.delete_message(chat_id=msg.from_user.id, message_id=message_id)
            return

    elif msg.document:
        file_id = msg.document.file_id
        await state.update_data(document=file_id)
        await msg.answer('Введите название: \n'
                         'Отменить: /break')
        await state.set_state(Chat.add_example3.state)


@dp.message_handler(state=Chat.add_example3.state)
async def get_title(msg: Message, state: FSMContext):
    message_id = (await state.get_data()).get('message_id')
    if 'break' in msg.text:
        await state.finish()
        await bot.delete_message(chat_id=msg.from_user.id, message_id=message_id)
        return
    data = await state.get_data()
    programming_language = data.get('programming_language')
    document = data.get('document')
    ExamplesManager().create(title=msg.text, programming_language=programming_language, filename=document)
    await msg.answer('Успешно!')
    await state.finish()
