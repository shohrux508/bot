import sqlite3

conn = sqlite3.connect('db.db')
cur = conn.cursor()
#keyboard_stack = {}
cur.execute(
    f'''CREATE TABLE IF NOT EXISTS users (user_id INTEGER, is_blocked INTEGER, is_admin INTEGER, full_name TEXT, phone TEXT, time TEXT, id INTEGER, language TEXT);''')
conn.commit()

cur.execute(
    f'''CREATE TABLE IF NOT EXISTS channels(channel_id INTEGER, user_id INTEGER, name TEXT, is_required INTEGER); ''')
conn.commit()
cur.execute(
    f'''CREATE TABLE IF NOT EXISTS sub_user(full_name TEXT, faculty TEXT, group_name TEXT, programming_language TEXT, user_id INTEGER, datetime TEXT, id INTEGER);''')
conn.commit()

cur.execute('''CREATE TABLE IF NOT EXISTS faculties(id INTEGER, title TEXT, language TEXT); ''')
conn.commit()
cur.execute(f'''CREATE TABLE IF NOT EXISTS programming_languages(id INTEGER, title TEXT)''')
conn.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS examples(id INTEGER, title TEXT, programming_language TEXT, filename TEXT)""")
conn.commit()
