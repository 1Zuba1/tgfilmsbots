#by @K1p1k#
#Downloaded from TG @KiTools#
#Leave this inscription#

from loader import dp, bot, admin_id
from aiogram import types
from myFilters.user import IsCode
from data.db import get_films, get_error_link_complaint_unix, update_error_link_complaint_unix, get_text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from time import time
from misc.chek_chennel import check as sub_check
from keybord_s.ohter import ikb_close
from keybord_s.user import kb_films, sub_list
from datetime import datetime, timedelta

#получение фильма по коду#
@dp.message_handler(IsCode())
async def get_FimsWithCode(message: types.Message):
    await message.delete()
    if await sub_check(user_id=message.from_user.id):
        await bot.send_message(chat_id=message.from_user.id, text='Вы не подписаны на канал(ы)❌\nПосле подписки повторите попытку👌', reply_markup=await sub_list())
        return


    film_data=await get_films(code=message.text)
    text_film=await get_text(type='text_text', text_type='film')
    text_film=text_film[0][0]
    me=await bot.get_me()
    text_film=str(text_film).replace('{username_bot}', me.mention)
    text_film=str(text_film).replace('{bot_id}', str(me.id))
    text_film=str(text_film).replace('{username}', message.from_user.mention)
    text_film=str(text_film).replace('{full_name}', message.from_user.full_name)
    text_film=str(text_film).replace('{user_id}', str(message.from_user.id)) 
    text_film=str(text_film).replace('{film_name}', film_data[0][1]) 
    
    ikb_films=await kb_films(name_films=film_data[0][1])
    await bot.send_photo(chat_id=message.from_user.id, photo=film_data[0][2], caption=text_film, reply_markup=ikb_films, parse_mode=types.ParseMode.HTML)

#Обработка кнопки "Одна из сыллок не работает❓"#
@dp.callback_query_handler(text='link_no_work')
async def Link_complaint(call: types.CallbackQuery):
    if await get_error_link_complaint_unix(user_id=call.from_user.id) == None or await get_error_link_complaint_unix(user_id=call.from_user.id) <= time():
        await call.message.answer('Мы отправили администратуру ошибку☑️', reply_markup=ikb_close)
        await bot.send_message(chat_id=admin_id, text=f'Пользователь [{call.from_user.full_name}](tg://user?id={call.from_user.id}) пожаловался то что одна из сыллок не работает❗️', parse_mode=types.ParseMode.HTML, reply_markup=ikb_close.row(InlineKeyboardButton(text='Проверить каналы⚛️', callback_data='check_chennel_admin')))
        timeub=datetime.now()+timedelta(hours=3)
        await update_error_link_complaint_unix(user_id=call.from_user.id, time_ub=timeub.timestamp())
    else:
        await call.answer('Вы уже жаловались❌')

#Автор: @K1p1k#
#Загружено с TG @KiTools#
#Оставь эту надпись#