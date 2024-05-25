from aiogram import types, Dispatcher
from data_base import sqlite_db
from keyboards import client_kb
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from datetime import date
from config import bot
import calc_tatu
todays = date.today()

class FSMAdmin(StatesGroup):
    chat_id = State()
    number = State()
    name = State()
    usl = State()
    date = State()


class calc(StatesGroup):
    size, design, style, placement = State(), State(), State(), State()

#start, help
async def command_start(message : types.Message, state : FSMContext):
    if sqlite_db.select_user(message.chat.id):
        await message.answer('Я персональный помощник *Имя тату мастера* чем я могу помочь?', reply_markup=client_kb.menu)
    else:
        async with state.proxy() as data:
            data['chat_id'] = message.chat.id
            data['name'] = message.from_user.first_name
        await FSMAdmin.number.set()
        await message.answer('Поделитесь с нами вашим номером, для дальнейшего взаимодействия', reply_markup=client_kb.number)

async def number(message : types.Message, state : FSMContext):
    async with state.proxy() as data:
        data['number'] = message.contact.phone_number
        sqlite_db.insert_user(data['chat_id'], data['number'], data['name'])
    await message.answer(f'Отлично {message.from_user.first_name}, доступ к боту получен /menu', reply_markup=client_kb.number_remove)
    await state.finish()

async def menu(message : types.Message):
    await message.answer('Я персональный помощник *Имя тату мастера* чем я могу помочь?', reply_markup=client_kb.menu)

async def sketches(callback : types.CallbackQuery):
    await callback.message.answer('Эскизы')
    mass = sqlite_db.select_all_sketches()
    for i in mass:
        await callback.message.answer_photo(i[3], caption=f'*{i[1]}*\n\n_{i[2]}_',parse_mode="Markdown", reply_markup=client_kb.sign_up(i[0]))
        await callback.answer()

async def sign_up(callback : types.CallbackQuery, state : FSMContext):
    record = sqlite_db.select_record(callback.message.chat.id)
    if record:
        await callback.message.answer(f'У вас уже есть запись\nНомер: {record[1]}\nИмя: {record[2]}\nУслуга: {record[3]}\nДата: {record[4]}', reply_markup=client_kb.delete)
        return 
    if callback.data == 'sign_up':
        usl = 'Эскиз под заказ(или доработка)'
    else:
        usl = callback.data.replace('sign_up_','')
        usl = sqlite_db.select_name(usl)
    async with state.proxy() as data:
        data['usl'] = usl
    await callback.message.delete()
    await callback.message.answer('Выбирай удобную для тебя дату(заполненные даты или выходные, не отображаются)', reply_markup=client_kb.dates_kb().add(client_kb.next_month))

async def date_user(callback : types.CallbackQuery, state : FSMContext):
    day = callback.data.replace('day_r_','')
    date = f'{day}-{todays.month}-{todays.year}'
    async with state.proxy() as data:
        data['date'] = date
        users_data = sqlite_db.select_user(callback.message.chat.id)
        sqlite_db.insert_record(users_data[0], users_data[1], users_data[2], data['usl'], data['date'])
    await callback.message.delete()

    await callback.message.answer(f'---Отлично, вот твоя запись---\nНомер: {users_data[1]}\nИмя: {users_data[2]}\nУслуга: {data["usl"]}\nДата: {data["date"]}', reply_markup=client_kb.delete)
    await bot.send_message(chat_id=692604698, text= f'---Новая запись---\nНомер: {users_data[1]}\nИмя: {users_data[2]}\nУслуга: {data["usl"]}\nДата: {data["date"]}')

async def date_n_user(callback : types.CallbackQuery, state : FSMContext):
    day = callback.data.replace('day_n_','')
    date = f'{day}-{todays.month+1}-{todays.year}'
    async with state.proxy() as data:
        data['date'] = date
        users_data = sqlite_db.select_user(callback.message.chat.id)
        sqlite_db.insert_record(users_data[0], users_data[1], users_data[2], data['usl'], data['date'])
    await callback.message.delete()
    await callback.message.answer(f'---Отлично, вот твоя запись---\nНомер: {users_data[1]}\nИмя: {users_data[2]}\nУслуга: {data["usl"]}\nДата: {data["date"]}', reply_markup=client_kb.delete)
    await state.finish()

async def next_month(callback : types.CallbackQuery, state : FSMContext):
    await callback.message.edit_text('Следующий месяц', reply_markup=client_kb.next_month_kb().add(client_kb.back_month))

async def delete_record(callback : types.CallbackQuery):
    sqlite_db.delete_record(callback.message.chat.id)
    await callback.message.delete()
    await callback.message.answer('Ваша запись удалена /menu')

async def calculate(callback : types.CallbackQuery):
    await callback.message.delete()
    await calc.size.set()
    await callback.message.answer('Для начала выбери размер будущей татуировки', reply_markup=client_kb.size)

async def design_tatu(callback : types.CallbackQuery, state : FSMContext):
    async with state.proxy() as data:
        data['size'] = callback.data.replace('size_','')
    await calc.next()
    await callback.message.edit_text('Нужно ли будет создавать или доделывать эскиз?', reply_markup=client_kb.design)

async def style_tatu(callback : types.CallbackQuery, state : FSMContext):
    async with state.proxy() as data:
        data['design'] = callback.data.replace('design_','')
    await calc.next()
    await callback.message.edit_text('Выбирай стиль тату', reply_markup=client_kb.style)

async def placement(callback : types.CallbackQuery, state : FSMContext):
    async with state.proxy() as data:
        data['style'] = callback.data.replace('style_','')
    await calc.next()
    await callback.message.edit_text('Выбирай место', reply_markup=client_kb.placement)

async def finish_tatu(callback : types.CallbackQuery, state : FSMContext):
    async with state.proxy() as data:
        data['placement'] = callback.data.replace('placement_','')
    total_price = calc_tatu.calculate_tattoo_cost(data['size'], data['design'], data['style'], data['placement'])
    r_total_price = total_price * 0.9
    await callback.message.edit_text(f'Стоимость тату: <s>{total_price}</s> <b>{r_total_price}</b>'
                                     f'\nТолько на первую татуировку, скидка 10% применина автоматически, успей записаться и урвать свою татку\n\n'
                                     , parse_mode='html')
    await callback.message.answer('Я персональный помощник *Имя тату мастера* чем я могу помочь?', reply_markup=client_kb.menu)
    await state.finish()

def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(number, content_types=['contact'], state=FSMAdmin.number)
    dp.register_message_handler(menu, commands=['menu'], state=None)

def register_callback_client(dp : Dispatcher):
    #dp.register_callback_query_handler(calc, lambda call: call.data == 'calc')
    dp.register_callback_query_handler(sketches, text = 'sketches')
    dp.register_callback_query_handler(sign_up, text_startswith = 'sign_up')
    dp.register_callback_query_handler(next_month, text = 'next_month_c')
    dp.register_callback_query_handler(sign_up, text = 'back_month_c')
    dp.register_callback_query_handler(date_user, text_startswith = 'day_r_')
    dp.register_callback_query_handler(delete_record, text = 'del')
    dp.register_callback_query_handler(date_n_user, text_startswith = 'day_n_')

    dp.register_callback_query_handler(calculate, text = 'calc')
    dp.register_callback_query_handler(design_tatu, text_startswith = 'size_', state = calc.size)
    dp.register_callback_query_handler(style_tatu, text_startswith = 'design_', state = calc.design)
    dp.register_callback_query_handler(placement, text_startswith = 'style_', state = calc.style)
    dp.register_callback_query_handler(finish_tatu, text_startswith = 'placement_', state = calc.placement)