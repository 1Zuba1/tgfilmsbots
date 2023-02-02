#by @K1p1k#
#Downloaded from TG @KiTools#
#Leave this inscription#

from aiogram import executor, types
from aiogram.dispatcher import FSMContext
from loader import dp, bot, admin_id
from handlers import dp
from keybord_s.ohter import ikb_close

#отмена любого состаяния#
@dp.callback_query_handler(text='cancellation_state', state='*')
async def cancellation_state(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.answer('Отмена❌')
    await call.message.delete()
    
#закрыть#
@dp.callback_query_handler(text='close_text')
async def cancellation_state(call: types.Message):
    await call.message.delete()

@dp.message_handler()
async def empty_command(message: types.Message):
    await message.delete()
    await message.answer('Такой команды нет🖍', reply_markup=ikb_close)

#уведомления о запуске#
async def satrt_nofication(self):
        me=await bot.get_me()
        for i in admin_id:
            try:
                await bot.send_message(chat_id=i, text=f'Bot worked {me.mention}', reply_markup=ikb_close)
            except:
                print(f'Bot worked {me.mention}')
                print(f'Вы не нажали /start в сеом боте!(id: {i})')
        print(f'Bot worked {me.mention}')

executor.start_polling(dp,  on_startup=satrt_nofication)

#Автор: @K1p1k#
#Загружено с TG @KiTools#
#Оставь эту надпись#