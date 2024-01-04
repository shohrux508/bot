# from keyboards.inline.user import api_token_btns
# from loader import dp, bot
# from aiogram.types import Message, CallbackQuery
# from aiogram.dispatcher.filters import Text
# from aiogram.dispatcher import FSMContext
# import requests as r
#
# from states.StatesGroup import APIToken
# auth_token = '74e074c29ea39ff25761f5c43aa60396a1239628'
#
# #login = r.request(method='POST', url='http://127.0.0.1:8000/api/v1/auth_token/token/login',
# #                  data={'password': '12345', 'username': 'shohrux'})
#
#
# @dp.message_handler(Text(contains='cars all'))
# async def cars(msg: Message):
#     list = (r.request(method='GET', url='http://127.0.0.1:8000/api/v1/cars/all/', headers={'authorization': f'Token {auth_token}'})).json()
#     await msg.answer(list)
#
# @dp.message_handler(Text(contains='/register_via_api'))
# async def answer(msg: Message, state: FSMContext):
#     await bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message_id)
#     message = await msg.answer('Введите ваше имя пользователя: \n'
#                                'Отменить: /break')
#     await state.update_data(message_id=message.message_id)
#     await state.set_state(APIToken.get_username.state)
#
#
# @dp.message_handler(state=APIToken.get_username.state)
# async def get_username(msg: Message, state: FSMContext):
#     await bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message_id)
#     message_id = (await state.get_data()).get('message_id')
#     if 'break' in msg.text:
#         await state.finish()
#         await bot.delete_message(chat_id=msg.from_user.id, message_id=message_id)
#         return
#     await state.update_data(username=msg.text)
#     await state.set_state(APIToken.get_password.state)
#     await bot.edit_message_text(chat_id=msg.from_user.id, message_id=message_id, text='Введите пароль: \n'
#                                                                                        'Отменить: /break')
#
#
# @dp.message_handler(state=APIToken.get_password.state)
# async def get_password(msg: Message, state: FSMContext):
#     await bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message_id)
#     message_id = (await state.get_data()).get('message_id')
#     if 'break' in msg.text:
#         await state.finish()
#         await bot.delete_message(chat_id=msg.from_user.id, message_id=message_id)
#         return
#     await state.update_data(password=msg.text)
#     username = (await state.get_data()).get('username')
#     await bot.edit_message_text(chat_id=msg.from_user.id, message_id=message_id, text=f'Имя пользователя: {username}\n'
#                                                                                       f'Пароль: {msg.text}',
#                                 reply_markup=api_token_btns())
#     await state.set_state(APIToken.finish.state)
#
#
# @dp.callback_query_handler(state=APIToken.finish.state)
# async def finish_st(call: CallbackQuery, state: FSMContext):
#     if 'break' in call.data:
#         await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
#     elif 'submit' in call.data:
#         data = await state.get_data()
#         username = data.get('username')
#         password = data.get('password')
#         api_token = r.request(method='POST', url='http://127.0.0.1:8000/api/v1/auth_token/token/login',
#                               data={'password': password, 'username': username})
#         await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
#                                     text=api_token.json()['auth_token'])
#     else:
#
#         await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text='/register')
#     await state.finish()
