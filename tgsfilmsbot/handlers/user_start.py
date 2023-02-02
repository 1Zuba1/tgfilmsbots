#by @K1p1k#
#Downloaded from TG @KiTools#
#Leave this inscription#

from loader import dp, bot, admin_id
from aiogram import types
from aiogram.dispatcher.filters import CommandStart, CommandHelp
from data.db import add_user, get_text
from keybord_s.user import kb_user

#комманда /start#
@dp.message_handler(CommandStart())
async def cmd_start(message: types.Message):
    if message.chat.type == types.ChatType.PRIVATE:
        try:
            await add_user(user_id=message.from_user.id, user_menotion=message.from_user.mention)
            await bot.send_message(chat_id=admin_id, text=f'<b>Новый пользователь <a href="tg://user?id={message.from_user.id}">{message.from_user.full_name}</a></b>', reply_markup=kb_user, parse_mode=types.ParseMode.HTML)
        except:
            pass
        text_start=await get_text(type='text_text', text_type='wellcome')
        text_start=text_start[0][0]
        me=await bot.get_me()
        text_start=str(text_start).replace('{username_bot}', me.mention)
        text_start=str(text_start).replace('{bot_id}', str(me.id))
        text_start=str(text_start).replace('{username}', message.from_user.mention)
        text_start=str(text_start).replace('{full_name}', message.from_user.full_name)
        text_start=str(text_start).replace('{user_id}', str(message.from_user.id)) 
        await message.answer(text=text_start, parse_mode=types.ParseMode.HTML, reply_markup=kb_user)

        
    
#Автор: @K1p1k#
#Загружено с TG @KiTools#
#Оставь эту надпись#