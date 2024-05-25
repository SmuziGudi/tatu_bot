from aiogram.utils import executor
from config import dp
import logging
from data_base import sqlite_db

logging.basicConfig(level=logging.INFO)

async def on_startup(_):
    print('Бот запущен')
    sqlite_db.sql_start()

from handlers import client, admin
admin.register_handlers_admin(dp)
admin.register_callback_admin(dp)
client.register_handlers_client(dp)
client.register_callback_client(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)