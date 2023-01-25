from loader import bot, dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from states import user as ustate
from keybord_s.user import kb_back
from keybord_s.ohter import ikb_close
from data.db import get_text, get_AllFranchise

@dp.message_handler(text='Поиск🔍')
async def search_kb(message: types.Message, state: FSMContext):
    await message.delete()
    msg=await message.answer('Убираем "Поиск🔍"', reply_markup=ReplyKeyboardRemove())
    await bot.delete_message(chat_id=message.from_user.id, message_id=msg.message_id)
    msg=await message.answer('<b>Отправь мне название кино🎫</b>', reply_markup=kb_back, parse_mode=types.ParseMode.HTML)
    async with state.proxy() as data:
        data['message_id']=msg.message_id
    await ustate.User_State.search_film.text.set()

@dp.message_handler(text='Франшиза🧩')
async def get_franchise(message: types.Message):
    await message.delete()
    text_franchise=await get_text(type='text_text', text_type='franchise')
    text_franchise=text_franchise[0][0]
    text_franchise_copy=text_franchise
    me=await bot.get_me()
    text_franchise=str(text_franchise).replace('{username_bot}', me.mention)
    text_franchise=str(text_franchise).replace('{bot_id}', str(me.id))
    text_franchise=str(text_franchise).replace('{username}', message.from_user.mention)
    text_franchise=str(text_franchise).replace('{full_name}', message.from_user.full_name)
    text_franchise=str(text_franchise).replace('{user_id}', str(message.from_user.id))
    catcher=str()
    for i in await get_AllFranchise():
        catcher+=f'🔰{i[0]} - {i[1]}\n'
    text_franchise=text_franchise.replace('{chapter}', catcher)
    await message.answer(text_franchise, reply_markup=ikb_close, parse_mode=types.ParseMode.HTML)
    
    
    #➖➖➖➖➖➖➖➖➖
    