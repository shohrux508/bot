from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from openpyxl import Workbook
from data.database import *
from datetime import datetime
import requests as r
from keyboards.default.main import StartKeyboard
from keyboards.inline.admin import AdminButton
from keyboards.one_time_keyboards import button
from loader import bot
from utils.db_api.check import is_member
from utils.db_api.manage import ManageUser, SubUserManager, Channel, MessageCheck, FacultyManager


def filter_data(data, function):
    response1 = data.replace(function, '')
    return response1


def get_users_as_text(sort_by, filter_by, page, paginate_by):
    sub_user = False
    if filter_by == 'admins':
        title = 'администраторов'
        cur.execute(f'''SELECT * FROM users WHERE is_admin > 0''')
    elif filter_by == 'blocked-users':
        title = 'заблокированных пользователей'
        cur.execute(f'''SELECT * FROM users WHERE is_blocked > 0''')
    elif filter_by == 'participants':
        sub_user = True
        title = 'участников олимпиады'
        cur.execute(f'''SELECT * FROM sub_user''')
    else:
        title = 'всех пользователей'
        cur.execute(f'''SELECT * FROM users''')
    users = cur.fetchall()
    if sub_user:
        if sort_by != False:
            if sort_by == 'name':
                users.sort(key=lambda users: users[0])
            elif sort_by == 'datetime':
                users.sort(key=lambda user: user[6])
            elif sort_by == 'id':
                users.sort(key=lambda user: user[7])
            else:
                pass
    else:
        if sort_by != False:
            if sort_by == 'name':
                users.sort(key=lambda users: users[1])
            elif sort_by == 'datetime':
                users.sort(key=lambda user: user[5])
            elif sort_by == 'id':
                users.sort(key=lambda user: user[6])
            else:
                pass
    count = 1
    full_text = []
    full_text.append(f'Список {title}: '
                     f'{datetime.now().strftime("%H:%M:%S")}\n')
    if sub_user:
        for user in users:
            text = (f'{user[6]}. Участник: {user[0]}\n'
                    f'Telegram ID: {user[4]}\n'
                    f'Факультет: {user[1]}\n'
                    f'Группа: {user[2]}\n'
                    f'Специальность: {user[3]}\n\n')
            full_text.append(text)
            count += 1
    else:
        for user in users:
            text = (f'{count}.{user[3]}\n'
                    f'Порядковый номер: {user[6]}\n'
                    f'Телеграм id: {user[0]}\n'
                    f'Номер телефонa: {user[4]}\n'
                    f'Дата Присоединения: {user[5]}\n'
                    f'\n'
                    f'------------------------------')
            full_text.append(text)
            count += 1
    chunked_lists = [full_text[i:i + paginate_by] for i in range(0, len(full_text), paginate_by)]
    chunked_lists[page - 1].append(f'Всего пользователей: {count - 1}\n\n'
                                   f'Страница: {page} из {len(chunked_lists)}')

    # chunked_lists[page-1].append(f'Общее количество {title}: {count - 1}\n')
    message = '\n'.join(full_text)
    message2 = '\n'.join(chunked_lists[page - 1])

    return message2


def manage_user_kb(user_id, msg_from_user_id):
    phone = (ManageUser(user_id).get(by=False, table_name="", data=""))[4]
    if "+" not in phone:
        phone = (f"+{phone}")
    ban = InlineKeyboardButton(text='Забанить ⛔️', callback_data=f"ban1+{user_id}")
    unban = InlineKeyboardButton(text='Разбанить ✅', callback_data=f"ban0+{user_id}")
    admin = InlineKeyboardButton(text='Администратор ✅️', callback_data=f"admin1+{user_id}")
    disadmin = InlineKeyboardButton(text='Удалить из админов ⛔️', callback_data=f"admin0+{user_id}")
    send_message_btn = InlineKeyboardButton(text='Написать 📝', callback_data=f'send_message_to_user{user_id}')
    find_profile_btn = InlineKeyboardButton(text='Найти профиль 🔍',
                                            url=f'https://t.me/{phone}')
    info_kb = InlineKeyboardMarkup().add(send_message_btn, find_profile_btn)
    if ManageUser(user_id).is_admin():
        info_kb.add(disadmin)
    else:
        info_kb.add(admin)

    if ManageUser(user_id).is_blocked():
        info_kb.add(unban)
    else:
        info_kb.add(ban)

    if user_id != msg_from_user_id:
        return info_kb
    else:
        return button('❌', '', 'delete_message')


def download_users_excel_file(filter_by):
    wb = Workbook()
    ws = wb.active
    if filter_by == 'participants':
        print("Participants")
        title = 'SubUsers'
        users = SubUserManager('').list()
    else:
        title = "Users"
        users = ManageUser(user_id='').list(select_id=False, filter_by=False, period=False)
    for user in users:
        ws.append(user)

    wb.save(f'data/excel/{title}{len(users)}.xlsx')
    return len(users)


def get_channel_as_text(channel_id):
    cur.execute(f'''SELECT * FROM channels WHERE channel_id = {channel_id}''')
    channel = cur.fetchone()
    text = (f'{channel[2]}.\n'
            f'Идентификационный номер: {channel[0]}')

    return text


def faculties_list_text():
    cur.execute(f'''SELECT * FROM faculties''')
    list = cur.fetchall()
    russian = []
    uzbek = []
    for i in list:
        if i[2] == 'ru':
            russian.append(i)
        else:
            uzbek.append(i)
    full_text = []
    full_text.append(f'Список факультетов: {datetime.now().strftime("%H:%M:%S")}\n'
                     f'Русский язык: \n')

    for i in russian:
        text = (f'Факультет номер {i[0]}: {i[1]}\n\n')
        full_text.append(text)
    full_text.append(f'____________________________')
    full_text.append(f'Узбекский язык: \n')
    for i in uzbek:
        text = (f'Fakultet N{i[0]}: {i[1]}\n\n')
        full_text.append(text)

    message = '\n'.join(full_text)
    return message


async def check_is_member(user_id):
    context = {}
    channels_keyboard = None
    keyboards = []
    final_status = True
    if ManageUser(user_id).language() == 'uz':
        result = "Botdan foydalanish uchun siz ushbu kanallarga obuna bo'lishingiz zarur!"
        btn = InlineKeyboardButton(text='Obuna bo\'ldim ✅', callback_data='check_subscription')
    else:
        result = "Вам необходимо подписаться на каналы чтобы пользоваться ботом:\n"
        btn = InlineKeyboardButton(text='Я подписался', callback_data='check_subscription')
    for channel in Channel(user_id=None).get_required_channels():
        channel_id = channel[0]
        status = await is_member(user_id=user_id, channel=channel_id)
        final_status *= status
        channel = await bot.get_chat(chat_id=channel_id)
        if not status:
            invite_link = await channel.export_invite_link()
            name = channel.title
            keyboards.append(InlineKeyboardButton(text=name, url=invite_link))

        channels_keyboard = InlineKeyboardMarkup().add(*keyboards).add(btn)
    if not final_status:
        context['keyboard'] = channels_keyboard
        context['response'] = result
        context['is_fully_subscribed'] = final_status
        await bot.send_message(chat_id=user_id, text=result, reply_markup=channels_keyboard)
    else:
        await bot.send_message(chat_id=user_id, text='Вы можете пользоваться ботом',
                               reply_markup=StartKeyboard(user_id).keyboard())


async def message_check(user_id, message, state):
    if MessageCheck(message).is_cancel():
        await state.finish()
        if ManageUser(user_id).language() == 'uz':
            await bot.send_message(chat_id=user_id, text='Bekor qilindi!')
        else:
            await bot.send_message(chat_id=user_id, text='Отменено!')
        return True


def manage_faculty_btns(language):
    ru, uz = AdminButton().faculties_kbs('delete-')
    if language == 'ru':
        return ru
    return uz
