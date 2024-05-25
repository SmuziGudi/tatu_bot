from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

token = '6622388421:AAEDXdXXL8EGhK8S61Dtl5u4Hh-aGLQuOlg'
bot = Bot(token=token)
dp = Dispatcher(bot, storage=storage)