from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import datetime
import calendar
from data_base import sqlite_db

this_date = datetime.date.today()
this_year = this_date.year
this_month = this_date.month
this_day = this_date.day
last_day = calendar.monthrange(this_date.year, this_date.month)

#buttons

add = InlineKeyboardButton(text='Добавить', callback_data='add')
delete = InlineKeyboardButton(text='Удалить', callback_data=f'delete_')
vue = InlineKeyboardButton(text='Просмотреть', callback_data='vue')

vue_graph = InlineKeyboardButton(text='Просмотреть график', callback_data='vue_graph')
add_weekend = InlineKeyboardButton(text='Добавить выходной', callback_data='add_weekend')
delete_week = InlineKeyboardButton(text='Удалить выходной', callback_data='delete_weekend')
delete_zapis = InlineKeyboardButton(text='Удалить', callback_data='deletezapis')
back = InlineKeyboardButton(text='Назад', callback_data='back')
bc = InlineKeyboardButton(text='Назад', callback_data='bc')
next_month = InlineKeyboardButton(text='➡️', callback_data='next_month')
back_month = InlineKeyboardButton(text='◀️', callback_data='back_month')

#markups

sketches_kb = InlineKeyboardMarkup(row_width=1).add(add, vue)
graph_kb = InlineKeyboardMarkup(row_width=1).add(vue_graph)
def delete_kb(id):
    return InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Удалить', callback_data=f'delete_{id}'))
# Управление записью
def zapis_markup(rec):
    del_btn = InlineKeyboardButton(text=f'Удалить', callback_data=f'deletezapis_{rec}')
    return InlineKeyboardMarkup(row_width=1).add(del_btn)
# Расписание
week_markup = InlineKeyboardMarkup(row_width=1).add(add_weekend, back)
week_markup_1 = InlineKeyboardMarkup(row_width=1).add(delete_week, back)
def dates_kb():
    days = []
    month_year = f'{this_month}-{this_year}'
    for i in range(this_day, last_day[1] + 1):
        week = sqlite_db.search_weekend(f'{i}-{this_month}-{this_year}')
        if week == 'y':
            days.append(InlineKeyboardButton(text=f'❌{str(i)}.{str(this_month)}', callback_data=f'date_❌{i}-{month_year}'))
        else:
            days.append(InlineKeyboardButton(text=f'{str(i)}.{str(this_month)}', callback_data=f'date_{i}-{month_year}'))
    return InlineKeyboardMarkup(row_width=5).add(*days)
def next_month_kb():
    days = []
    next_month_last_day = calendar.monthrange(this_year, this_month + 1)[1]
    month_year = f'{this_month + 1}-{this_year}'
    for i in range(1, next_month_last_day + 1):
        week = sqlite_db.search_weekend(f'{i}-{this_month+1}-{this_year}')
        if week == 'y':
            days.append(InlineKeyboardButton(text=f'❌{str(i)}.{str(this_month + 1)}', callback_data=f'date_❌{i}-{month_year}'))
        else:
            days.append(InlineKeyboardButton(text=f'{str(i)}.{str(this_month + 1)}', callback_data=f'date_{i}-{month_year}'))
    return InlineKeyboardMarkup(row_width=5).add(*days)