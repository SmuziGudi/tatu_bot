import sqlite3 as sq
import datetime
import calendar
from config import bot

base = sq.connect('admin.db')
cur = base.cursor()

def sql_start():   
 
    if base:
        print('База данных подключена')
    cur.execute('CREATE TABLE IF NOT EXISTS users(CHAT_ID INTEGER, Number INTEGER, Name TEXT, usl TEXT, Date TEXT)')
    cur.execute('CREATE TABLE IF NOT EXISTS graph(date TEXT, weekend TEXT, chat_id INTEGER)')
    cur.execute('CREATE TABLE IF NOT EXISTS users_data(CHAT_ID INTEGER, Number INTEGER, Name TEXT)')
    cur.execute('CREATE TABLE IF NOT EXISTS sketches(id INTEGER PRIMARY KEY, name TEXT NOT NULL, description TEXT NOT NULL, photo TEXT NOT NULL)')
    cur.execute('CREATE TABLE IF NOT EXISTS admin_info(CHAT_ID INTEGER)')
    base.commit()

# Добавление записи
def insert_record(CHAT_ID, Number, name, usl, Date):
    cur.execute('INSERT INTO users(CHAT_ID, Number, Name, usl, Date) VALUES(?, ?, ?, ?, ?)', (CHAT_ID, Number, name, usl, Date))
    cur.execute('INSERT INTO graph(date, weekend, chat_id) VALUES(?, ?, ?)', (Date, 'n', CHAT_ID))
    base.commit()

def select_record(CHAT_ID):
    for i in cur.execute('SELECT * FROM users WHERE CHAT_ID = ?', tuple([CHAT_ID])).fetchall():
        return i

def delete_record(CHAT_ID):
    cur.execute('DELETE FROM graph WHERE CHAT_ID = ?', tuple([CHAT_ID]))
    cur.execute('DELETE FROM users WHERE CHAT_ID = ?', tuple([CHAT_ID]))
# Поиск выходного
def search_weekend(date):
    for i in cur.execute('SELECT * FROM graph WHERE date = ?', tuple([date])).fetchall():
        return (i[1])
    
# Добавление выходного
def insert_weekend(date):
    graph_info = cur.execute('SELECT * FROM graph WHERE date = ?', tuple([date])).fetchall()
    if graph_info:
        for i in graph_info:
            chatid = i[2]
            bot.send_message(chatid, 'Ваша запись отменена, попробуйте перезаписаться /menu')
            cur.execute('UPDATE graph SET weekend = ? WHERE date = ?', ('y', date))
            cur.execute('DELETE FROM users WHERE date = ?', (date,))
    else:
        cur.execute('INSERT INTO graph(date, weekend) VALUES(?, ?)', (date, 'y'))
    base.commit()

# Поиск записи по дате
def search_record(date):
    for i in cur.execute('SELECT * FROM users WHERE Date = ?', tuple([date])).fetchall():
        return i
def search_record_admin(date):
    users = []
    rec = []
    for i in cur.execute('SELECT * FROM graph WHERE date = ?', tuple([date])).fetchall():
        users.append(i[2])
    for i in users:
        rec.append(cur.execute('SELECT * FROM users WHERE CHAT_ID = ?', tuple([i])).fetchall())
    return rec

    

def delete_weekend(date):
    cur.execute('DELETE FROM graph WHERE date = ?', (date,))
    base.commit()

# Добавление пользователя
def insert_user(CHAT_ID, Number, Name):
    if cur.execute('SELECT * FROM users_data WHERE CHAT_ID = ?', tuple([CHAT_ID])).fetchall():
        return False
    else:
        cur.execute('INSERT INTO users_data(CHAT_ID, Number, Name) VALUES(?, ?, ?)', (CHAT_ID, Number, Name))
        base.commit()

# Проверка пользователя
def select_user(CHAT_ID):
    for i in cur.execute('SELECT * FROM users_data WHERE CHAT_ID = ?', tuple([CHAT_ID])).fetchall():
        return i

# Добавление эскиза
async def insert_sketch(name, description, photo):
    cur.execute('INSERT INTO sketches(name, description, photo) VALUES(?, ?, ?)', (name, description, photo))
    base.commit()

# Демонстрация эскизов
def select_all_sketches():
    mass = []
    for i in cur.execute('SELECT * FROM sketches').fetchall():
        mass.append(i)
    return mass

def select_name(id):
    for i in cur.execute('SELECT * FROM sketches WHERE id = ?', tuple([id])).fetchall():
        return i[1]

# Удаление эскиза
def delete_sketch(id):
    cur.execute('DELETE FROM sketches WHERE id = ?', (id,))
    base.commit()

# Добавление админа
def insert_admin(CHAT_ID):
    cur.execute('INSERT INTO admin_info(CHAT_ID) VALUES(?)', (CHAT_ID,))
    base.commit()

# Поиск админа
def chatid(message):
    admins = []
    for i in cur.execute('SELECT * FROM admin_info CHAT_ID').fetchall():
        admins.append(i[0])
    if message in admins:
        return True
    else:
        return False
