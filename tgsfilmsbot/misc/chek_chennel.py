from loader import bot, admin_id
from myFilters.user import IsCode
from data.db import get_AllChennel
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keybord_s.ohter import ikb_close

async def check(user_id):
    data_chennel=await get_AllChennel()
    for i in data_chennel:
        try:
            status=await bot.get_chat_member(chat_id=i[0], user_id=user_id)
            if status.status == 'left':
                return True
        except:
            await bot.send_message(chat_id=admin_id, text=f'Похоже этот канал удалил нас запустите "Проверку каналов"\nЧто бы проверить меня на наличие прав\nИндификатор: {i[0]}\nНазвание: {i[1]}\nСыллка: {i[2]}', reply_markup=ikb_close.row(InlineKeyboardButton(text='Проверить каналы⚛️', callback_data='check_chennel_admin')))
    return False