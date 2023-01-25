#by @K1p1k#
#Downloaded from TG @KiTools#
#Leave this inscription#

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import *

#Connect к боту#
storage=MemoryStorage()
bot=Bot(token)
dp=Dispatcher(bot, storage=storage)
bot_version='1.5'

#Автор: @K1p1k#
#Загружено с TG @KiTools#
#Оставь эту надпись#