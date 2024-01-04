import curses.ascii
import datetime

from data.config import ADMINS
from data.database import *


def create_id(table, id_index):
    cur.execute(f"""SELECT * FROM {table}""")
    result = cur.fetchall()
    id_index = int(id_index)
    if result == []:
        id = 1
    else:
        id = result[-1][id_index] + 1
    return id


def ban(user_id):
    cur.execute(f'''SELECT is_blocked FROM users WHERE user_id = "{user_id}" ''')
    block = (cur.fetchone())[0]
    block = int(block) + 1
    if block > 3:
        return False
    cur.execute(f'''UPDATE users SET is_blocked = "{block}" ''')
    conn.commit()
    return True


def search_user(phone_or_id: str or int):
    id = phone_or_id
    if "+" not in id:
        user = ManageUser(id).get(by=False, table_name='', data='')
    else:
        user = ManageUser(id).get(by=True, table_name='phone', data=id)
    if user is None:
        return False
    else:
        if user[1]:
            status = 'Заблокирован'
        else:
            status = 'Имеет доступ к боту'
        if user[2]:
            pos = 'Администратор'
        else:
            pos = 'Пользователь'
        text = (f'{pos}-{user[3]}: {user[6]}\n'
                f'Идентификационный номер: {user[0]}\n'
                f'Статус: {status}\n'
                f'Дата присоединения: {user[5]}\n'
                f'Номер телефона: {user[4]}')
        response = [user[0], text]

        return response


class ManageUser():
    def __init__(self, user_id):
        self.user_id = user_id

    def new(self, full_name, phone, is_admin, is_blocked, language):
        if "'" in full_name:
            full_name = full_name.replace("'", '"')
        if str(self.user_id) in ADMINS:
            is_admin = 3
        id = create_id(table='users', id_index='6')
        now = datetime.datetime.now().strftime("%D(%H:%M:%S)")
        cur.execute(
            f'''INSERT INTO users VALUES('{self.user_id}', '{is_blocked}', '{is_admin}', '{full_name}', '{phone}', '{now}', '{id}', '{language}')''')
        conn.commit()
        return ()

    def get(self, by: bool, table_name: str, data: str or int):
        if by:
            cur.execute(f'''SELECT * FROM users WHERE {table_name} = "{data}" ''')
        else:
            cur.execute(f'''SELECT * FROM users WHERE user_id = {self.user_id}''')
        user = cur.fetchone()
        return user

    def block(self, status):
        cur.execute(f'''UPDATE users SET is_blocked = '{status}' WHERE user_id = {self.user_id}''')
        conn.commit()

        return ()

    def admin(self, position):
        cur.execute(f'''UPDATE users SET is_admin = '{position}' WHERE user_id = {self.user_id} ''')
        conn.commit()
        return ()

    def list(self, select_id, filter_by, period):
        if filter_by == 'admin':
            cur.execute(f'''SELECT * FROM users WHERE is_admin > 0''')
        elif filter_by == 'blocked':
            cur.execute(f'''SELECT * FROM users WHERE is_blocked != 0''')
        else:
            cur.execute(f'''SELECT * FROM users''')

        users = cur.fetchall()
        list = []
        if select_id:
            for user in users:
                list.append(user[0])

        else:
            list = users

        if period:
            start = int(period[0])
            end = int(period[1])
            list = list[start:end]

        return list

    def is_user(self):
        cur.execute(f'''SELECT * FROM users WHERE user_id = '{self.user_id}' ''')
        user = cur.fetchone()
        if user is None:
            return False
        else:
            return True

    def is_admin(self):
        cur.execute(f'''SELECT is_admin FROM users WHERE user_id = {self.user_id}''')
        response = cur.fetchone()
        if response is None:
            return False
        elif response[0] > 0:
            return True
        else:
            return False

    def is_blocked(self):
        cur.execute(f'''SELECT is_blocked FROM users WHERE user_id = '{self.user_id}' ''')
        response = cur.fetchone()
        if response is None:
            return False
        elif response[0] != 0:
            return True
        else:
            return False

    def set_language(self, language):
        cur.execute(f'''UPDATE users SET language = "{language}" WHERE user_id = "{self.user_id}" ''')
        conn.commit()
        return

    def set_phone(self, phone):
        cur.execute(f"""UPDATE users SET phone = '{phone}' WHERE user_id = '{self.user_id}' """)
        conn.commit()
        return

    def language(self):
        cur.execute(f'''SELECT language FROM users WHERE user_id = "{self.user_id}" ''')
        lang = cur.fetchone()
        if lang is None:
            lang = 'ru'
        else:
            lang = lang[0]
        return lang


class SubUserManager():

    def __init__(self, user_id):
        self.user_id = user_id

    def create(self, full_name, faculty, group, programming_language):
        if '"' in full_name:
            full_name = full_name.replace('"', "'")
        if '"' in group:
            group = group.replace('"', "'")

        time = datetime.datetime.now().strftime("%d:%H:%M:%S")
        id = create_id('sub_user', 6)
        cur.execute(
            f'''INSERT INTO sub_user VALUES("{full_name}", "{faculty}",  "{group}", "{programming_language}", "{self.user_id}", "{time}", "{id}")''')
        conn.commit()
        return id

    def update(self, full_name, faculty, group, programming_language, id):
        if '"' in full_name:
            full_name = full_name.replace('"', "'")
        if '"' in group:
            group = group.replace('"', "'")
        time = datetime.datetime.now().strftime("%d:%H:%M:%S")
        cur.execute(f'''DELETE FROM sub_user WHERE id = {id}''')
        conn.commit()
        cur.execute(
            f'''INSERT INTO sub_user VALUES("{full_name}", "{faculty}",  "{group}", "{programming_language}", "{self.user_id}", "{time}", "{id}")''')
        conn.commit()
        return id

    def list(self):
        cur.execute(f'''SELECT * FROM sub_user''')
        list = cur.fetchall()
        return list

    def get(self, by: bool, table_name: str, data: str or int):
        if by:
            cur.execute(f'''SELECT * FROM sub_user WHERE "{table_name}" = "{data.lower()}" ''')
            user = cur.fetchall()
        else:
            cur.execute(f'''SELECT * FROM sub_user WHERE user_id = {self.user_id}''')
            user = cur.fetchone()
        return user

    def is_registered(self):
        cur.execute(f'''SELECT * FROM sub_user WHERE user_id = {self.user_id}''')
        user = cur.fetchone()
        if user:
            return user
        else:
            return False

    def remove(self):
        cur.execute(f'''DELETE FROM sub_user WHERE user_id = "{self.user_id}" ''')
        conn.commit()
        return


class Check():
    def __init__(self, user_id):
        self.user_id = user_id


class MessageCheck():

    def __init__(self, message):
        self.message = message

    def is_cancel(self):
        if self.message is None:
            return False
        elif 'отменить' in self.message.lower() or 'bekor qilish' in self.message.lower() or 'break' in self.message.lower():
            return True
        else:
            return False

    def is_skip(self):
        if 'пропустить' in self.message.lower():
            return True
        else:
            return False


class CallBackData_():
    def __init__(self, user_id, message_id):
        self.user_id = user_id
        self.message_id = message_id

    def new(self, data):
        id = create_id(table='callback_data', id_index=0)
        cur.execute(f'''INSERT INTO callback_data VALUES('{id}', '{self.user_id}', '{self.message_id}', '{data}')''')
        conn.commit()
        return True

    def delete(self, id):
        cur.execute(f'''DELETE FROM callback_data WHERE id = {id}''')
        conn.commit()
        return True

    def get(self):
        cur.execute(f'''SELECT data FROM callback_data WHERE message_id = {self.message_id}''')
        data = cur.fetchone()
        return data


class Channel():

    def __init__(self, user_id):
        self.user_id = user_id

    def create(self, channel_id, name, is_required):
        cur.execute(f'''INSERT INTO channels VALUES('{channel_id}', '{self.user_id}', '{name}', '{is_required}');''')
        conn.commit()
        return id

    def get(self, channel_id):
        cur.execute(f'''SELECT * FROM channels WHERE channel_id = "{channel_id}"''')
        channel = cur.fetchone()
        return channel

    def remove(self, channel_id):
        cur.execute(f'''DELETE FROM channels WHERE channel_id = "{channel_id}" ''')
        conn.commit()
        print(f'removed{channel_id}')
        return True

    def list(self):
        cur.execute(f'''SELECT * FROM channels''')
        list = cur.fetchall()
        return list

    def set_required(self, status: int, channel_id: int):
        cur.execute(f'''UPDATE channels SET is_required = {status} WHERE channel_id = {channel_id}''')
        conn.commit()
        return True

    def get_required_channels(self):
        cur.execute(f"""SELECT * FROM channels WHERE is_required = 1""")
        channels = cur.fetchall()
        return channels


class FacultyManager():

    def create(self, title, language):
        id = create_id('faculties', 0)
        print(id, title, language)
        cur.execute(f'''INSERT INTO faculties VALUES('{id}', '{title}', '{language}');''')
        conn.commit()
        return

    def get(self, id):
        cur.execute(f'''SELECT * FROM faculties WHERE id = {id}''')
        got = cur.fetchone()
        return got

    def select(self, id, language):
        cur.execute(f'''SELECT title FROM faculties WHERE id = {id} and language = {language}''')
        title = cur.fetchone()[0]
        return title

    def list(self, language):
        if language == 'all':
            cur.execute(f'''SELECT * FROM faculties WHERE language = "ru" ''')
            ru = cur.fetchall()
            cur.execute(f'''SELECT * FROM faculties WHERE language = "uz" ''')
            uz = cur.fetchall()
            return ru, uz
        cur.execute(f'''SELECT * FROM faculties WHERE language = "{language}" ''')
        list = cur.fetchall()
        return list

    def remove(self, id):
        cur.execute(f'''DELETE FROM faculties WHERE id = "{id}" ''')
        conn.commit()
        return True


class DirectionManager():

    def create(self, title):
        id = create_id('programming_languages', 0)
        cur.execute(f'''INSERT INTO programming_languages VALUES('{id}', '{title}')''')
        conn.commit()
        return

    def list(self, select_title):
        if select_title:
            cur.execute(f'''SELECT title FROM programming_languages''')
        else:
            cur.execute(f'''SELECT * FROM programming_languages''')
        list = cur.fetchall()
        return list

    def get(self, id):
        cur.execute(f'''SELECT * FROM programming_langues WHERE id = {id}''')
        data = cur.fetchall()
        return data

    def remove(self, id):
        cur.execute(f'''DELETE FROM programming_languages WHERE id = {id}''')
        conn.commit()
        return


class VideoUrlsManager():

    def create(self, title: str, programming_language: str, url: str):
        id = create_id(table='video_lessons', id_index=0)
        try:
            cur.execute(
                f'''INSERT INTO video_lessons VALUES('{id}', '{title}', 'not given', '{programming_language}', '{url}');''')
            conn.commit()
        except:
            return False
        return True

    def remove(self, id):
        try:
            cur.execute(f'''DELETE FROM video_lessons WHERE id = {id}''')
            conn.commit()
        except:
            return False
        return True

    def get(self, id: int, by: bool, filter_by, data):
        if by:
            cur.execute(f'''SELECT * FROM video_lessons WHERE "{filter_by}" = "{data}" ''')
        else:
            cur.execute(f'''SELECT * FROM video_lessons WHERE id = {id}''')
        try:
            response = cur.fetchall()
        except:
            return None
        return response

    def list(self, filter_by):
        if filter_by == 'all':
            cur.execute(f'''SELECT * FROM video_lessons''')
        list = cur.fetchall()
        return list

    def check(self, programming_language):
        cur.execute(f'''SELECT * FROM video_lessons WHERE programming_language = "{programming_language}" ''')
        response = cur.fetchall()
        if response == []:
            return False
        else:
            return True


class ExamplesManager():

    def create(self, title, programming_language, filename):
        id = create_id(table='examples', id_index=0)
        cur.execute(f'''INSERT INTO examples VALUES("{id}", "{title}", "{programming_language}", "{filename}"); ''')
        conn.commit()

    def get(self, id):
        cur.execute(f'''SELECT * FROM examples WHERE id = {id}''')
        response = cur.fetchone()
        return response

    def remove(self, id):
        cur.execute(f'''DELETE FROM examples WHERE id = {id}''')
        conn.commit()
        return

    def list(self, programming_language):
        cur.execute(f'''SELECT * FROM examples WHERE programming_language = "{programming_language}" ''')
        list = cur.fetchall()
        return list

    def drop(self):
        cur.execute("""DELETE FROM examples""")
        conn.commit()
        return
