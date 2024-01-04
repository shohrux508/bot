from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from loader import bot
from utils.db_api.check import is_required
from utils.db_api.manage import FacultyManager, DirectionManager, ExamplesManager


class AdminButton():

    def send_message_kb(self):
        btn1 = InlineKeyboardButton(text='Всем пользователям', callback_data='message_filter_by=all')
        btn2 = InlineKeyboardButton(text='Выбрать факультет', callback_data='message_filter_by=faculty')
        btn3 = InlineKeyboardButton(text='Выбрать направление', callback_data='message_filter_by=direction')
        keyboard = InlineKeyboardMarkup().add(btn1).add(btn2).add(btn3)
        return keyboard

    def send_message_by_faculty(self, language):
        list = FacultyManager().list(language)
        btn_list = []
        for i in list:
            btn = InlineKeyboardButton(text=i[1], callback_data=f'send_message_by_faculty={i[0]}')
            btn_list.append(btn)
        keyboard = InlineKeyboardMarkup().add(*btn_list)
        return keyboard

    def send_message_by_direction(self):
        list = DirectionManager().list(select_title=False)
        btn_list = []
        for i in list:
            btn = InlineKeyboardButton(text=i[1], callback_data=f'send_message_by_programming_language={i[1]}')
            btn_list.append(btn)
        keyboard = InlineKeyboardMarkup().add(*btn_list)
        return keyboard

    def direction_kbs(self):
        list = DirectionManager().list(select_title=False)
        btn_list = []
        for i in list:
            btn = InlineKeyboardButton(text=i[1], callback_data=f'{i[1]}')
            btn_list.append(btn)
        break_btn = InlineKeyboardButton(text='Отменить', callback_data='break')
        keyboard = InlineKeyboardMarkup().add(*btn_list).add(break_btn)
        return keyboard

    def examples_kbs(self, programming_language):
        list = ExamplesManager().list(programming_language=programming_language)
        btn_list = []
        print(list)
        if list == []:
            return False
        for i in list:
            btn = InlineKeyboardButton(text=i[1], callback_data=f'example={i[0]}')
            btn_list.append(btn)
        break_btn = InlineKeyboardButton(text='Отменить', callback_data='break')
        keyboard = InlineKeyboardMarkup().add(*btn_list).add(break_btn)
        return keyboard

    def faculties_kbs(self, function):
        ru, uz = FacultyManager().list(language='all')
        ru_btn_list = []
        uz_btn_list = []
        for i in ru:
            btn = InlineKeyboardButton(text=f'{i[1]}', callback_data=f'{function}faculty={i[0]}')
            ru_btn_list.append(btn)
        for i in uz:
            btn = InlineKeyboardButton(text=f'{i[1]}', callback_data=f'{function}faculty={i[0]}')
            uz_btn_list.append(btn)
        break_btn = InlineKeyboardButton(text='Отменить', callback_data='break')
        keyboard1 = InlineKeyboardMarkup().add(*ru_btn_list).add(break_btn)
        keyboard2 = InlineKeyboardMarkup().add(*uz_btn_list).add(break_btn)
        return keyboard1, keyboard2

    def manage_example_single(self, id):
        btn1 = InlineKeyboardButton(text='Удалить', callback_data=f'delete-example={id}')
        btn2 = InlineKeyboardButton(text='Просмотреть', callback_data=f'see-example={id}')
        keyboard = InlineKeyboardMarkup().add(btn2).add(btn1)
        return keyboard

    def manage_sent_messages(self, message_id, count):
        btn1 = InlineKeyboardButton(text='Изменить сообщение', callback_data=f'edit-public-msgs{message_id}+{count}')
        btn2 = InlineKeyboardButton(text='Удалить сообщение', callback_data=f'delete-public-msgs{message_id}+{count}')
        keyboard = InlineKeyboardMarkup().add(btn1).add(btn2)
        return keyboard

    def manage_sent_message(self, user_id, message_id):
        btn1 = InlineKeyboardButton(text='Изменить сообщение', callback_data=f'edit-private-msg{user_id}+{message_id}')
        btn2 = InlineKeyboardButton(text='Удалить сообщение', callback_data=f'delete-private-msg{user_id}+{message_id}')
        keyboard = InlineKeyboardMarkup().add(btn1).add(btn2)
        return keyboard

    def manage_users_list(self, sort_by, filter_by, page, paginate_by):
        str = f'{sort_by}+{filter_by}+{page}+{paginate_by}'
        btn1 = InlineKeyboardButton(text='⬅️', callback_data=f'prev-page{str}')
        btn2 = InlineKeyboardButton(text='➡️', callback_data=f'next-page{str}')
        btn3 = InlineKeyboardButton(text='Все пользователи', callback_data=f'filter-by-users')
        btn4 = InlineKeyboardButton(text='Участники Олимпиады', callback_data=f'filter-by-participants')
        btn5 = InlineKeyboardButton(text='Администраторы👨‍🚀', callback_data=f'filter-by-admins')
        btn6 = InlineKeyboardButton(text='Чёрный список', callback_data=f'filter-by-blocked-users')
        btn7 = InlineKeyboardButton(text='Искать 🔍', callback_data=f'search-user')
        btn8 = InlineKeyboardButton(text='Обновить', callback_data=f'refresh')
        keyboard = InlineKeyboardMarkup().add(btn1, btn6, btn2).add(btn3).add(btn4).add(btn5).add(btn6).add(btn7)
        return keyboard

    def download_users(self):
        btn = InlineKeyboardButton(text='Все пользователи бота', callback_data='download=all')
        btn1 = InlineKeyboardButton(text='Участники Олимпиады', callback_data='download=participants')
        keyboard = InlineKeyboardMarkup().add(btn).add(btn1)
        return keyboard

    async def manage_channel(self, channel_id):
        if is_required(channel_id):
            btn = InlineKeyboardButton(text='Удалить из списка обязательной подписки❌',
                                       callback_data=f'set_required0+{channel_id}')
        else:
            btn = InlineKeyboardButton(text='Добавить в список обязательной подписки✅',
                                       callback_data=f'set_required1+{channel_id}')
        link = await bot.export_chat_invite_link(chat_id=channel_id)
        btn3 = InlineKeyboardButton(text='Открыть ', url=link)
        btn4 = InlineKeyboardButton(text='Удалить', callback_data=f'delete-channel{channel_id}')
        add = InlineKeyboardButton(text='Добавить канал', callback_data='add-channel')
        keyboard = InlineKeyboardMarkup().add(btn3, btn4).add(btn).add(add)
        return keyboard

    def manage_examples(self):
        btn = InlineKeyboardButton(text='Добавить', callback_data='add-example')
        btn1 = InlineKeyboardButton(text='Просмотреть список', callback_data='see-list')
        keyboard = InlineKeyboardMarkup().add(btn1).add(btn)
        return keyboard

    def manage_programming_languages(self):
        btn = InlineKeyboardButton(text='Список языков', callback_data='programming-languages-list')
        btn2 = InlineKeyboardButton(text='Добавить язык программирования', callback_data='add-programming-language')
        keyboard = InlineKeyboardMarkup().add(btn).add(btn2)
        return keyboard

    def manage_faculties(self):
        btn = InlineKeyboardButton(text='Список факультетов', callback_data='faculties-list')
        btn2 = InlineKeyboardButton(text='Добавить факультет', callback_data='add-faculty')
        keyboard = InlineKeyboardMarkup().add(btn).add(btn2)
        return keyboard
