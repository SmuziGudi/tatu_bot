from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

token = 'your_token'
bot = Bot(token=token)
dp = Dispatcher(bot, storage=storage)
