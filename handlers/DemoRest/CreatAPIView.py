# import requests as r
#
# from keyboards.inline.user import save_datas
# from keyboards.one_time_keyboards import button
# from loader import dp, bot
# from aiogram.types import Message, CallbackQuery
# from aiogram.dispatcher.filters import Text
# from aiogram.dispatcher import FSMContext
#
# from states.StatesGroup import CarCreate
#
# auth_token = '74e074c29ea39ff25761f5c43aa60396a1239628'
#
#
# @dp.message_handler(Text(contains='/car_create'))
# async def new_car(msg: Message, state: FSMContext):
#     message = await msg.answer('Vin: \n'
#                                '/break')
#     await state.update_data(message_id=message.message_id)
#     await state.set_state(CarCreate.get_vin.state)
#
#
# @dp.message_handler(state=CarCreate.get_vin.state)
# async def get_vin(msg: Message, state: FSMContext):
#     message_id = (await state.get_data()).get('message_id')
#     await bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message_id)
#     if 'break' in msg.text:
#         await state.finish()
#         await bot.delete_message(chat_id=msg.from_user.id, message_id=message_id)
#         return
#     await state.update_data(vin=msg.text)
#     await state.set_state(CarCreate.get_color.state)
#     await bot.edit_message_text(chat_id=msg.from_user.id, message_id=message_id, text='Color: \n'
#                                                                                       '/break')
#
#
# @dp.message_handler(state=CarCreate.get_color.state)
# async def get_color(msg: Message, state: FSMContext):
#     message_id = (await state.get_data()).get("message_id")
#     await bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message_id)
#     if 'break' in msg.text:
#         await state.finish()
#         await bot.delete_message(chat_id=msg.from_user.id, message_id=message_id)
#         return
#     await state.update_data(color=msg.text)
#     await state.set_state(CarCreate.get_brand.state)
#     await bot.edit_message_text(chat_id=msg.from_user.id, message_id=message_id, text='Brand: \n'
#                                                                                       '/break')
#
#
# @dp.message_handler(state=CarCreate.get_brand.state)
# async def get_brand(msg: Message, state: FSMContext):
#     message_id = (await state.get_data()).get("message_id")
#     await bot.delete_message(chat_id=msg.from_user.id, message_id=msg.message_id)
#     if 'break' in msg.text:
#         await state.finish()
#         await bot.delete_message(chat_id=msg.from_user.id, message_id=message_id)
#         return
#     await state.update_data(brand=msg.text)
#     await state.set_state(CarCreate.get_car_type.state)
#
#     await bot.edit_message_text(chat_id=msg.from_user.id, message_id=message_id, text='Car type: \n',
#                                 reply_markup=car_types())
#
#
# @dp.callback_query_handler(state=CarCreate.get_car_type.state)
# async def get_cart_type(call: CallbackQuery, state: FSMContext):
#     data = await state.get_data()
#     vin = data.get('vin')
#     color = data.get("color")
#     brand = data.get('brand')
#     car_type = call.data
#     await state.update_data(car_type=car_type)
#     await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=f'vin: {vin}\n'
#                                                                                                     f'color: {color}\n'
#                                                                                                     f'brand: {brand}\n'
#                                                                                                     f'car-type: {car_type}',
#                                 reply_markup=save_datas())
#
#     await state.set_state(CarCreate.finish.state)
#
# @dp.callback_query_handler(state=CarCreate.finish.state)
# async def finish_st(call: CallbackQuery, state: FSMContext):
#     data = await state.get_data()
#     vin = data.get('vin')
#     color = data.get("color")
#     brand = data.get('brand')
#     car_type = data.get('car_type')
#     action = call.data
#     response = CarCreateAPI(vin, color, brand, car_type)
#     if response == '201':
#         response = 'Successfully Created'
#     await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id, text=response)
#     await state.finish()

