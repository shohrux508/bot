from aiogram.dispatcher.handler import CancelHandler
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import dp, bot
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types
from utils.db_api.manage import Channel, ManageUser
from utils.db_api.check import is_member

keyboards = []
channels_keyboard = None
message_ids = {}


class BigBrother(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        if update.message:
            ID = update.message.from_user.id
            if update.message.text:
                if update.message.text in ['/start', '/help'] or update.message.text.startswith('+998'):
                    return
            elif update.message.contact:
                return
        elif update.callback_query:
            ID = update.callback_query.from_user.id
            if update.callback_query.data.startswith(f"set_language"):
                return
        else:
            return
        if ManageUser(ID).language() == 'uz':
            result = "Botdan foydalanish uchun siz ushbu kanallarga obuna bo'lishingiz zarur!"
            btn = InlineKeyboardButton(text='Obuna bo\'ldim ✅', callback_data='check_subscription')
        else:
            result = "Вам необходимо подписаться на каналы чтобы пользоваться ботом:\n"
            btn = InlineKeyboardButton(text='Я подписался', callback_data='check_subscription')
        final_status = True
        for channel in Channel(user_id=None).get_required_channels():
            channel_id = channel[0]
            status = await is_member(user_id=ID, channel=channel_id)
            final_status *= status
            channel = await bot.get_chat(chat_id=channel_id)

            if not status:
                invite_link = await channel.export_invite_link()
                name = channel.title
                keyboards.append(InlineKeyboardButton(text=name, url=invite_link))

        channels_keyboard = InlineKeyboardMarkup().add(*keyboards).add(btn)

        if not final_status:
            if update.message:
                await update.message.answer(result, disable_web_page_preview=True, reply_markup=channels_keyboard)
            elif update.callback_query:
                if update.callback_query.data.startswith('check'):
                    try:
                        await bot.edit_message_text(chat_id=update.callback_query.from_user.id,
                                                    message_id=update.callback_query.message.message_id,
                                                    text='Возможно вы не подписались !\n'
                                                         'Пожалуйста перепроверьте', reply_markup=channels_keyboard)
                    except:
                        await update.callback_query.answer('Пожалуйста подпишитесь на каналы!')
                else:
                    await update.callback_query.answer('Вам необходимо подписаться на каналы!')
                    await bot.send_message(chat_id=update.callback_query.from_user.id, text=result,
                                           disable_web_page_preview=True, reply_markup=channels_keyboard)
            keyboards.clear()
            raise CancelHandler()
