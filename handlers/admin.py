from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from keyboards import admin_kb
from data_base import sqlite_db
from config import dp, bot


class FSMAdmin(StatesGroup):
    chat_id = State()
    photo = State()
    name = State()
    description = State()
    date = State()
    records = State()

# Админ панель
async def admin_logging(message: types.Message):
    chat_id = message.chat.id
    admin = sqlite_db.chatid(chat_id)
    if admin:
        await message.answer(f'Здравствуйте, {message.from_user.full_name}, вы вошли в админ панель')
        await message.answer('Эскизы', reply_markup=admin_kb.sketches_kb)
        await message.answer('Расписание', reply_markup=admin_kb.graph_kb)
    else:
        await message.answer(f'Здравствуйте, {message.from_user.full_name}, вы не админ')

# Добавление админа
async def admin_register(message: types.Message):
    chat_id = message.chat.id
    admin = sqlite_db.chatid(chat_id)
    sqlite_db.insert_admin(chat_id)
    if admin:
        await message.answer(f'Вы уже админ /admin')
    else:
        await message.answer(f'Теперь вы админ и имеете доступ к админ панели /admin')

# Добавление эскиза
async def sketch_add(callback_query: types.CallbackQuery):
    await FSMAdmin.photo.set()
    await callback_query.message.answer('Отправьте фото эскиза')

@dp.message_handler(state=FSMAdmin.photo, content_types=['photo']) # type: ignore
async def sketch_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id
    await FSMAdmin.next()
    await message.answer('Отправьте название эскиза')

async def sketch_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAdmin.next()
    await message.answer('Отправьте описание эскиза')

async def sketch_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await sqlite_db.insert_sketch(data['name'], data['description'], data['photo'])
    await state.finish()
    await message.answer('Эскиз добавлен')

# Просмотр эскизов
async def vue(callback_query: types.CallbackQuery):
    mass = sqlite_db.select_all_sketches()
    for i in mass:
        await callback_query.message.answer_photo(i[3], caption=f'*{i[1]}*\n\n_{i[2]}_',parse_mode="Markdown", reply_markup=admin_kb.delete_kb(i[0]))
        await callback_query.answer()

# Удаление эскиза
async def delete(callback_query: types.CallbackQuery):
    sqlite_db.delete_sketch(callback_query.data.replace('delete_',''))
    await callback_query.message.delete()
    await callback_query.message.answer('Эскиз удален')

# График
async def vue_graph(callback_query: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback_query.message.delete()
    await callback_query.message.answer('График', reply_markup=admin_kb.dates_kb().add(admin_kb.next_month))
    await callback_query.answer()
    
async def next_month(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text('График', reply_markup=admin_kb.next_month_kb().add(admin_kb.back_month))
    await callback_query.answer()

async def rec_week(callback_query: types.CallbackQuery, state: FSMContext):
    await FSMAdmin.date.set()
    date = callback_query.data.replace("date_","")
    # date_week =sqlite_db.search_weekend(date)
    records = sqlite_db.search_record(date)
    if records != None:
        await callback_query.message.delete()
        rec_adm = sqlite_db.search_record_admin(date)
        async with state.proxy() as data:
            data['date'] = date
        
        for i in rec_adm:
            await callback_query.message.answer(f'Дата: *{i[0][4]}*\nНомер: *{i[0][1]}*\nИмя: *{i[0][2]}*\nЧат ID: *{i[0][0]}*\nУслуга: *{i[0][3]}*',
                                        reply_markup=admin_kb.zapis_markup(i[0][0]).add(admin_kb.bc),
                                        parse_mode="Markdown")
        await state.finish()
    else:
        async with state.proxy() as data:
            data['date'] = date
        await callback_query.message.edit_text(f'Дата: *{date}*',
                                           reply_markup=admin_kb.week_markup,
                                           parse_mode="Markdown")
        await callback_query.answer()

async def rec_week_n(callback_query: types.CallbackQuery, state: FSMContext):
    await FSMAdmin.date.set()
    date = callback_query.data.replace("date_","")
    async with state.proxy() as data:
        data['date'] = date
    await callback_query.message.edit_text(f'Дата: *{date}*',
                                           reply_markup=admin_kb.week_markup,
                                           parse_mode="Markdown")
    await callback_query.answer()

async def week_date(callback_query: types.CallbackQuery, state: FSMContext):
    await FSMAdmin.date.set()
    date = callback_query.data.replace("date_❌","")
    async with state.proxy() as data:
        data['date'] = date
    await callback_query.message.edit_text(f'Дата: *❌{date}*',
                                           reply_markup=admin_kb.week_markup_1,
                                           parse_mode="Markdown")

# Добавление выходного
async def add_week(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        sqlite_db.insert_weekend(data['date'])
    
    await callback_query.message.edit_text(f'Выходной *{data["date"]}* добавлен', parse_mode="Markdown")
    await state.finish()

async def del_week(callback_query: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        sqlite_db.delete_weekend(data['date'])
    
    await callback_query.message.edit_text(f'Выходной *{data["date"]}* удален', parse_mode="Markdown")
    await state.finish()




async def deletezapis(callback_query: types.CallbackQuery):
    zap = callback_query.data.replace("deletezapis_","")
    sqlite_db.delete_record(zap)
    await bot.send_message(zap, 'Запись удалена, можете перезаписаться /menu', parse_mode="Markdown")

    await callback_query.message.edit_text(f'Запись удалена, пользователь оповещён', parse_mode="Markdown")

def register_handlers_admin(dp : Dispatcher):
    dp.register_message_handler(admin_logging, commands=['admin'])
    dp.register_message_handler(admin_register, commands=['admin_register'])

def register_callback_admin(dp : Dispatcher):
    dp.register_callback_query_handler(vue, text='vue')
    dp.register_callback_query_handler(delete, text_startswith='delete_')
    dp.register_callback_query_handler(deletezapis, text_startswith='deletezapis')

    dp.register_callback_query_handler(vue_graph, text='vue_graph')
    dp.register_callback_query_handler(week_date, text_startswith='date_❌')
    dp.register_callback_query_handler(rec_week_n, text_startswith='date_n')
    dp.register_callback_query_handler(rec_week, text_startswith='date_')
    dp.register_callback_query_handler(vue_graph, text='back',state=FSMAdmin.date)
    dp.register_callback_query_handler(vue_graph, text='bc')
    dp.register_callback_query_handler(add_week, text='add_weekend', state=FSMAdmin.date)
    dp.register_callback_query_handler(del_week, text='delete_weekend', state=FSMAdmin.date)
    dp.register_callback_query_handler(next_month, text='next_month')
    dp.register_callback_query_handler(vue_graph, text='back_month')

    dp.register_callback_query_handler(sketch_add, text='add')
    dp.register_callback_query_handler(sketch_photo, state=FSMAdmin.photo)
    dp.register_message_handler(sketch_name, state=FSMAdmin.name)
    dp.register_message_handler(sketch_description, state=FSMAdmin.description)