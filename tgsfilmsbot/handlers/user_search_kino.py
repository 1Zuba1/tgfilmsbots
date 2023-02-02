#by @K1p1k#
#Downloaded from TG @KiTools#
#Leave this inscription#

from loader import bot, dp, rate_searsh
from aiogram import types
from aiogram.dispatcher import FSMContext
from keybord_s.user import kb_films, sub_list, kb_user
from misc.chek_chennel import check as sub_check
from data.db import add_historyInSearch
from states import user as ustate
from misc.search_film import search

async def anti_flood(*args, **kwargs):
    m = args[0]
    await m.answer(f'Фильм можно найти раз в {rate_searsh} секунд😪', reply_markup=kb_user)
    state = dp.current_state(chat=m.from_user.id, user=m.from_user.id)
    await state.set_state(None)

async def spisok_number_to60():
    counter_number=int()
    list_rt=str()
    while counter_number != 60:
        counter_number+=1
        list_rt+=f'{str(counter_number)} '
    list_rt=list_rt.split()
    return list_rt

@dp.message_handler(state=ustate.User_State.search_film.text)
@dp.throttled(anti_flood, rate=rate_searsh)
async def search_kino_parser(message: types.Message, state: FSMContext):
    await message.delete()
    async with state.proxy() as data:
        await bot.delete_message(chat_id=message.from_user.id, message_id=data['message_id'])
    if message.text == 'Отмена❌':
        await message.answer('Отмена❌', reply_markup=kb_user)
        await state.finish()
        return

    if await sub_check(user_id=message.from_user.id):
        await bot.send_message(chat_id=message.from_user.id, text='Вы не подписаны на канал(ы)❌\nПосле подписки повторите попытку👌', reply_markup=await sub_list())
        return

    try:
        data_film=await search(name_film=message.text)
        await bot.send_photo(chat_id=message.from_user.id, photo=data_film.photo_, caption=f'<b>🎥{data_film.type_kino_}: </b><code>{data_film.name_film_}</code>\n\n<b>👁Основной жанр: {data_film.genre_}\n\n👥{data_film.text_autor_}: {data_film.director_}\n\n🔗Длительность: {data_film.length_}</b>', reply_markup=await kb_films(name_films=data_film.name_film_, user_id=message.from_user.id), parse_mode=types.ParseMode.HTML)
        await add_historyInSearch(name=data_film.name_film_)
        await message.answer(f'Следующий запрос можно будет сделать через {rate_searsh}😴', reply_markup=kb_user)
    except:
        await message.answer('Нам не удолось найти фильм😥')
        await message.answer(f'Следующий запрос можно будет сделать через {rate_searsh}😴', reply_markup=kb_user)
    await state.finish()
#Автор: @K1p1k#
#Загружено с TG @KiTools#
#Оставь эту надпись#
