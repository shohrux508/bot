from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from utils.db_api.manage import ManageUser, DirectionManager, FacultyManager, VideoUrlsManager


def share_language(user_id):
    btn1 = InlineKeyboardButton(text='Узбекский язык 🇺🇿', callback_data=f'set_language{user_id}+uz')
    btn2 = InlineKeyboardButton(text='Русския язык 🇷🇺', callback_data=f'set_language{user_id}+ru')
    keyboard = InlineKeyboardMarkup().add(btn2).add(btn1)
    return keyboard


def register_btn():
    web_app = WebAppInfo()
    button = InlineKeyboardButton(text='Press', web_app=WebAppInfo(), url='https://google.com')

    keyboard = InlineKeyboardMarkup().add(button)
    return keyboard


def faculty_kbs(language):
    list = FacultyManager().list(language)
    btn_list = []
    for i in list:
        print(i)
        btn = InlineKeyboardButton(text=i[1], callback_data=f'{i[0]}+{language}')
        btn_list.append(btn)
    if language == 'uz':
        cancel = 'Bekor qilish'
    else:
        cancel = 'Отменить'
    cancel_kb = InlineKeyboardButton(text=cancel, callback_data='break')
    keyboard = InlineKeyboardMarkup().add(*btn_list).add(cancel_kb)
    return keyboard


def programming_languages_kbs(user_id):
    list = DirectionManager().list(select_title=False)
    btn_list = []
    for i in list:
        btn = InlineKeyboardButton(text=(i[1]).title(), callback_data=(i[1]).lower())
        btn_list.append(btn)
    keyboard = InlineKeyboardMarkup().add(*btn_list)
    if ManageUser(user_id).language() == 'uz':
        keyboard.add(InlineKeyboardButton(text='Bekor qilish', callback_data='break'))
    else:
        keyboard.add(InlineKeyboardButton(text='Отменить', callback_data='break'))
    return keyboard


def finish_registration_kb(language):
    if language == 'ru':
        kb = InlineKeyboardButton(text='Подтвердить сохранение', callback_data='submit')
        kb2 = InlineKeyboardButton(text='Начать заново', callback_data='retry')
        kb3 = InlineKeyboardButton(text='Отменить регистратцию', callback_data='break')
    else:
        kb = InlineKeyboardButton(text='Tasdiqlash', callback_data='submit')
        kb2 = InlineKeyboardButton(text='Boshidan boshlash', callback_data='retry')
        kb3 = InlineKeyboardButton(text='Bekor qilish', callback_data='break')

    return InlineKeyboardMarkup().add(kb).add(kb2).add(kb3)




def examples():
    list = DirectionManager().list(select_title=True)
    btn_list = []
    for data in list:
        btn = InlineKeyboardButton(text=f'{data}', callback_data=f'example={data}')
        btn_list.append(btn)
    keyboard = InlineKeyboardMarkup().add(*btn_list)
    return keyboard


def api_token_btns():
    btn1 = InlineKeyboardButton(text='Зарегаться', callback_data='submit')
    btn2 = InlineKeyboardButton(text='Отменить', callback_data='break')
    btn3 = InlineKeyboardButton(text='Начать заново', callback_data='retry')
    keyboard = InlineKeyboardMarkup().add(btn1).add(btn2).add(btn3)
    return keyboard

def save_datas():
    btn1 = InlineKeyboardButton(text='Сохранить', callback_data='save')
    btn2 = InlineKeyboardButton(text='Отменить', callback_data='cancel')
    keyboard = InlineKeyboardMarkup().add(btn1).add(btn2)
    return keyboard


def car_list_btns():
    list = CarsListAPI()
    btn_list = []
    for i in list:
        btn = InlineKeyboardButton(text=f'{i["vin"]}', callback_data=f'{i["id"]}')
        btn_list.append(btn)
    keyboard = InlineKeyboardMarkup().add(*btn_list)
    return keyboard

