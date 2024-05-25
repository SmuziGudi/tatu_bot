from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import datetime
import calendar
from data_base import sqlite_db


number = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
number.add(KeyboardButton('Поделиться номером', request_contact=True))
number_remove = ReplyKeyboardRemove()

menu = InlineKeyboardMarkup(row_width=2)
gps = InlineKeyboardButton(text='Местоположение', url='https://www.google.com/maps')
sketch = InlineKeyboardButton(text='Мои эскизы', callback_data='sketches')
connect = InlineKeyboardButton(text='Написать напрямую', url='t.me/SmuziRalShit')
calc = InlineKeyboardButton(text='Калькулятор тату', callback_data='calc')
back = InlineKeyboardButton(text='Назад', callback_data='back')
sign_up = InlineKeyboardButton(text='Записаться', callback_data='sign_up')
menu.add(gps, sketch, connect, calc, sign_up)

delete = InlineKeyboardMarkup(row_width=1)
delete.add(InlineKeyboardButton(text='Удалить', callback_data='del'))

def sign_up(id):
    return InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Записаться', callback_data=f'sign_up_{id}'))

# Расписание
this_date = datetime.date.today()
this_year = this_date.year
this_month = this_date.month
this_day = this_date.day
last_day = calendar.monthrange(this_date.year, this_date.month)
next_month = InlineKeyboardButton(text='➡️', callback_data='next_month_c')
back_month = InlineKeyboardButton(text='◀️', callback_data='back_month_c')
def dates_kb():
    dates_kb = []
    for i in range(this_day, last_day[1] + 1):
        week = sqlite_db.search_weekend(f'{i}-{this_month}-{this_year}')
        if week == 'y':
            next
        else:
            dates_kb.append(InlineKeyboardButton(text=f'{str(i)}.{str(this_month)}', callback_data=f'day_r_{i}'))
    return InlineKeyboardMarkup(row_width=5).add(*dates_kb)

def next_month_kb():
    dates_kb = []
    next_month_last_day = calendar.monthrange(this_year, this_month + 1)[1]
    for i in range(1, next_month_last_day + 1):
        week = sqlite_db.search_weekend(f'{i}-{this_month+1}-{this_year}')
        if week == 'y':
            next
        else:
            dates_kb.append(InlineKeyboardButton(text=f'{str(i)}.{str(this_month + 1)}', callback_data=f'day_n_{i}'))
    return InlineKeyboardMarkup(row_width=5).add(*dates_kb)





#calc
size = InlineKeyboardMarkup(row_width=1)
small = InlineKeyboardButton(text='5 - 10 см', callback_data='size_small')
medium = InlineKeyboardButton(text='10 - 20 см', callback_data='size_medium')
large = InlineKeyboardButton(text='20 - 30 см', callback_data='size_large')
size.add(small, medium, large)

design = InlineKeyboardMarkup(row_width=1)
sketch_design = InlineKeyboardButton(text='Требуется', callback_data='design_sketch_design')
null = InlineKeyboardButton(text='Выберу готовый', callback_data='design_null')
design.add(sketch_design, null)

style = InlineKeyboardMarkup(row_width=1)
realistic_style = InlineKeyboardButton(text='Реализм', callback_data='style_realistic_style')
geometric_style = InlineKeyboardButton(text='Геометрия', callback_data='style_geometric_style')
minimalist_style = InlineKeyboardButton(text='Минимализм', callback_data='style_minimalist_style')
several = InlineKeyboardButton(text='Совместить несколько', callback_data='style_several')
style.add(realistic_style, geometric_style, minimalist_style, several)

placement = InlineKeyboardMarkup(row_width=1)
forearm_placement = InlineKeyboardButton(text='Руки, плечи, ноги', callback_data='placement_forearm_placement')
back_placement = InlineKeyboardButton(text='Спина, грудь, живот', callback_data='placement_back_placement')
chest_placement = InlineKeyboardButton(text='Колени, локти, лицо', callback_data='placement_chest_placement')
leg_placement = InlineKeyboardButton(text='Интим', callback_data='placement_leg_placement')
placement.add(forearm_placement, back_placement, chest_placement, leg_placement)
