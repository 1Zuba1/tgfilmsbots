#by @K1p1k#
#Downloaded from TG @KiTools#
#Leave this inscription#

from loader import bot, dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from myFilters.admin import IsAdminM
from states import admin as astate
from data.db import add_film, only_list, get_AllUser, delete_Film, add_Chennel, delete_Chennel, update_kbname_player, update_wellcome_text, get_AllText, get_AllSearch, get_Allplayer, get_AllFilms, get_AllChennel, get_AllFranchise, add_franchise, delete_franchise, get_Allfavourite, cs, sql
from keybord_s.admin import get_Player_menu
from keybord_s.ohter import ikb_back, ikb_close, ikb_back_oikb
import json
from datetime import datetime

@dp.channel_post_handler(text='/get_id')
async def get_id(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=message.chat.id)

#рассылка#
@dp.message_handler(IsAdminM(), state=astate.Admin_State.myling_list.text, content_types=types.ContentTypes.ANY)
async def myling_list(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data_user=await only_list(await get_AllUser(type='user_id'))
        count_accept=0
        count_error=0
        ikb=types.InlineKeyboardMarkup(row_width=1)
        for i in data['ikb_list']:
            ikb.row(i)
        await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text=f'<b>Данные о рассылки\nТекст: "{message.text}"\n✅Успешно: {count_accept}\n❌Ошибки: {count_error}</b>', parse_mode=types.ParseMode.HTML)
        for i in data_user:
            try:
                count_accept+=1
                await bot.copy_message(chat_id=i, from_chat_id=message.from_user.id, message_id=message.message_id, reply_markup=ikb)
                await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text=f'<b>Данные о рассылки\nТекст: "{message.text}"\n✅Успешно: {count_accept}\n❌Ошибки: {count_error}</b>', parse_mode=types.ParseMode.HTML)
            except:
                count_error+=1
                await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text=f'<b>Данные о рассылки\nТекст: "{message.text}"\n✅Успешно: {count_accept}\n❌Ошибки: {count_error}</b>', parse_mode=types.ParseMode.HTML)
        await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text=f'<b>Данные о рассылки\nТекст: "{message.text}"\n✅Успешно: {count_accept}\n❌Ошибки: {count_error}\nРассылка завершенна🔔</b>', parse_mode=types.ParseMode.HTML, reply_markup=ikb_close)
    await state.finish()

#обработка текста на добавление кнопки#
@dp.message_handler(IsAdminM(), state=astate.Admin_State.myling_list.add_ikb.text)
async def add_ikb_milling_text(message: types.Message, state: FSMContext):
    await message.delete()
    ikb=types.InlineKeyboardMarkup(row_width=1)
    ikb.row(types.InlineKeyboardButton(text='Назад🔙', callback_data='back_to_text_milling'))
    async with state.proxy() as data:
        data['text_ikb']=message.text
        await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text='Отправь мне ссылку на кнопке📝', reply_markup=ikb)
    await astate.Admin_State.myling_list.add_ikb.url.set()
    
@dp.message_handler(IsAdminM(), state=astate.Admin_State.myling_list.add_ikb.url)
async def add_ikb_milling_url(message: types.Message, state: FSMContext):
    await message.delete()
    ikb=types.InlineKeyboardMarkup(row_width=1)
    ikb.row(types.InlineKeyboardButton(text='Добавить кнопку▶️', callback_data='add_ikb_milling_admin'))
    ikb.row(ikb_back_oikb)
    
    async with state.proxy() as data:
        try:
            ikb_test_ikb=types.InlineKeyboardMarkup().row({'text' : data['text_ikb'], 'url' : message.text})
            test_msg=await message.answer('Тест кнопки...', reply_markup=ikb_test_ikb)
            await test_msg.delete()
            data['ikb_list'].append({'text' : data['text_ikb'], 'url' : message.text})
            try:
                await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'],  text='Кнопка добавлена➕\n\nХорошо отправь текст для рассылки✒️\nМожно использовать стандартную разметку✂️', reply_markup=ikb)
            except:
                pass
        except:
            try:
                await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'],  text='Кнопка не добавлена(не правильная сыллка)❌\n\nХорошо отправь текст для рассылки✒️\nМожно использовать стандартную разметку✂️', reply_markup=ikb)
            except:
                pass
            pass

    await astate.Admin_State.myling_list.text.set()

#получения кода от фильма#
@dp.message_handler(IsAdminM(), state=astate.Admin_State.add_film.code)
async def state_add_film_code(message: types.Message, state: FSMContext):
    
    async with state.proxy() as data:
        data['code']=message.text
        await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text='Хорошо теперь отправь мне название🎫', reply_markup=ikb_back)
    await astate.Admin_State.add_film.name.set()

#получение название от фильма#
@dp.message_handler(IsAdminM(),state=astate.Admin_State.add_film.name)
async def state_add_film_name(message: types.Message, state: FSMContext):
    await message.delete()
    async with state.proxy() as data:
        data['name']=message.text
    await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text='Отлично теперь отправь мне фотографии для обложки📌', reply_markup=ikb_back)
    await astate.Admin_State.add_film.priew.set()

#палучение обложки и сохранение данных#
@dp.message_handler(IsAdminM(), state=astate.Admin_State.add_film.priew, content_types=types.ContentTypes.PHOTO)
async def state_add_film_priew(message: types.Message, state: FSMContext):
    await message.delete()
    async with state.proxy() as data:
        await bot.delete_message(chat_id=message.chat.id, message_id=data['message_id'])
        try:
            await add_film(code=data['code'], name=data['name'], priv=message.photo[-1].file_id)
            await message.answer_photo(photo=message.photo[-1].file_id, caption=f'📌Фильм добавлен\n🔑Код: <code>{data["code"]}</code>\n🎫Название: {data["name"]}', reply_markup=ikb_close, parse_mode=types.ParseMode.HTML)
        except:
            await message.answer('Скорее всего этот код уже добавлен\nОтмена❌', reply_markup=ikb_close)
    await state.finish()

#если не фотография#
@dp.message_handler(IsAdminM(), state=astate.Admin_State.add_film.priew)
async def state_add_film_priew_no_photo(message: types.Message, state: FSMContext):
    await message.delete()
    async with state.proxy() as data:
        try:
            await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text='Жду фотографию😡\nОтлично теперь отправь мне фотографии для обложки📌', reply_markup=ikb_back)
        except:
            pass

#удаления фильма#
@dp.message_handler(IsAdminM(), state=astate.Admin_State.delete_film.code)
async def delete_film(message: types.Message, state: FSMContext):
    await message.delete()
    async with state.proxy() as data:
        try:
            chennel_identifier=int(message.text)
        except:
            chennel_identifier=message.text
        if await delete_Film(code=chennel_identifier):
            await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text='Успешно удалено❎', reply_markup=ikb_close)
            await state.finish()
        else:
            try:
                await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text='Нет токого кода❌', reply_markup=ikb_back)
            except:
                pass

#добавление канал#
@dp.message_handler(IsAdminM(), state=astate.Admin_State.add_chennel.username)
async def add_chennel(message: types.Message, state: FSMContext):
    await message.delete()
    async with state.proxy() as data:
        try:
            chennel_identifier=int(message.text)
        except:
            chennel_identifier=message.text
        try:
            await bot.get_chat_member(chat_id=chennel_identifier, user_id=message.from_user.id)
            chat=await bot.get_chat(chat_id=chennel_identifier)
            me=await bot.get_me()
            link_chat=await bot.create_chat_invite_link(chat_id=chennel_identifier, name=f'Вход от {me.mention}')
            try:
                await add_Chennel(chennel_identifier=chennel_identifier, name=chat.full_name, link=link_chat.invite_link)
                await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text='Канал успешно добавлен✅', reply_markup=ikb_close)
                await state.finish()
            except:
                await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text='Этот канал уже был добавлен🫤', reply_markup=ikb_back)
        except:
            try:
                await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text='Извините у меня там нет прав "просматривать участников" и "управления сыллками"❌', reply_markup=ikb_back)
            except:
                pass

#Удаление канала#
@dp.message_handler(IsAdminM(), state=astate.Admin_State.delete_chennel.username)
async def delete_chennel(message: types.Message, state: FSMContext):
    await message.delete()
    async with state.proxy() as data:
        if await delete_Chennel(chennel_identifier=message.text):
            await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text='Канал удален успешно✅', reply_markup=ikb_close)
            await state.finish()
        else:
            await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text='Извините вы не добавляли такого канал❌', reply_markup=ikb_back)
    
@dp.message_handler(IsAdminM(), state=astate.Admin_State.chennger_kbname_player.text)
async def chennger_kbname_player(message: types.Message, state: FSMContext):
    await message.delete()
    async with state.proxy() as data:
        await update_kbname_player(player_name=data['name_kb'], kb=message.text)
        await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id1'], text='Кнопка изменена успешно✅', reply_markup=ikb_close)
        await bot.edit_message_reply_markup(chat_id=message.from_user.id, message_id=data['message_id2'], reply_markup=await get_Player_menu())
        await state.finish()

#объект который добавить в франшизы#
@dp.message_handler(IsAdminM(), state=astate.Admin_State.add_franchise.name_obj)
async def add_franchise_obj(message: types.Message, state: FSMContext):
    await message.delete()
    async with state.proxy() as data:
        await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text='Хорошо отправь мне описание📝\n\nМожно ипользовать разметку HTML✂️', reply_markup=ikb_back)
        data['obj']=message.text
    await astate.Admin_State.add_franchise.description.set()

#удвление франшизы#
@dp.message_handler(IsAdminM(), state=astate.Admin_State.delete_franchise.name_obj)
async def delete_franchise_obj(message: types.Message, state: FSMContext):
    await message.delete()
    async with state.proxy() as data:
        if await delete_franchise(obj=message.text):
            await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text='Объект франшизы успешно удален🗑', reply_markup=ikb_close)
            await state.finish()

        else:
            try:
                await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text='Токого объекта нету❌', reply_markup=ikb_back)
            except:
                pass
        

#описание который добавить в франшизн#
@dp.message_handler(IsAdminM(), state=astate.Admin_State.add_franchise.description)
async def add_franchise_description(message: types.Message, state: FSMContext):
    await message.delete()
    async with state.proxy() as data:
        try:
            await add_franchise(obj=data['obj'], description=message.text)
            await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text='Франшиза успешно добавлена✅', reply_markup=ikb_close)
            await state.finish()
        except:
            await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text='Отправь мне объект для франшизы🌀\nЭтот объект уже есть❌', reply_markup=ikb_back)
            await astate.Admin_State.add_franchise.name_obj.set()


#Измение текста приведствия#
@dp.message_handler(IsAdminM(), state=astate.Admin_State.chennger_wellcome_text.text)
async def chennger_wellcome_text(message: types.Message, state: FSMContext):
    await message.delete()
    async with state.proxy() as data:
        try:
            await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text=message.text, parse_mode=types.ParseMode.HTML)
            await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text='Успешно изминил текст приветствия✅', reply_markup=ikb_close)
            await state.finish()
            await update_wellcome_text(text_type='wellcome', text=message.text)
        except:
            try:
                await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text='Не правильная разметка HTML✂️', reply_markup=ikb_back)
            except:
                pass

#Ищминение текста фильма#
@dp.message_handler(IsAdminM(), state=astate.Admin_State.chennger_film_text.text)
async def chennger_wellcome_text(message: types.Message, state: FSMContext):
    await message.delete()
    async with state.proxy() as data:
        try:
            await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text=message.text, parse_mode=types.ParseMode.HTML)
            await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text='Успешно изминил текст фильма✅', reply_markup=ikb_close)
            await update_wellcome_text(text_type='film', text=message.text)
            await state.finish()
        except:
            try:
                await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text='Не правильная разметка HTML✂️', reply_markup=ikb_back)
            except:
                pass

@dp.message_handler(IsAdminM(), state=astate.Admin_State.chennger_franchise_text.text)
async def chennger_franchise_text(message: types.Message, state: FSMContext):
    await message.delete()
    async with state.proxy() as data:
        if message.text.find('{chapter}') != -1:
            try:
                await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text=message.text, parse_mode=types.ParseMode.HTML)
                await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text='Успешно изминил текст франшизи✅', reply_markup=ikb_close)
                await update_wellcome_text(text_type='franchise', text=message.text)
                await state.finish()
            except:
                try:
                    await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text='Не правильная разметка HTML✂️', reply_markup=ikb_back)
                except:
                    pass
        else:
            await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text='Нет форматирование с <code>{chapter}</code>❌', parse_mode=types.ParseMode.HTML, reply_markup=ikb_back)

#экспорт конфига#
@dp.message_handler(IsAdminM(), commands=['export'])
async def export_cfg(message: types.Message):
    dict_cfg=dict()
    dict_cfg['user_data']=await get_AllUser()
    dict_cfg['text_data']=await get_AllText()
    dict_cfg['search_data']=await get_AllSearch()
    dict_cfg['player_data']=await get_Allplayer()
    dict_cfg['films_data']=await get_AllFilms()
    dict_cfg['chennel_data']=await get_AllChennel()
    dict_cfg['franchise_data']=await get_AllFranchise()
    dict_cfg['favourites_data']=await get_Allfavourite()
    patch_json=f'data//cash_config//config{str(datetime.now())}.json'.replace(':', '.')
    file_json=open(file=patch_json, mode='w', encoding='UTF-8')
    json_dump = json.dump(dict_cfg, file_json, indent=2)
    file_json.close()
    await bot.send_document(chat_id=message.from_user.id, document=open(file=patch_json, mode='rb'), reply_markup=ikb_close)

#импорт конфига#
@dp.message_handler(IsAdminM(), text='/import')
async def export_cfg(message: types.Message, state: FSMContext):
    masg=await message.answer('Отправь мне файл .json📥', reply_markup=ikb_back)
    async with state.proxy() as data:
        data['message_id']=masg.message_id
    await astate.Admin_State.import_cfg.file.set()

#получение конфига#
@dp.message_handler(IsAdminM(), state=astate.Admin_State.import_cfg.file, content_types=types.ContentTypes.DOCUMENT)
async def get_filte_import(message: types.Message, state: FSMContext):
    await message.delete()
    if message.document.mime_type != 'application/json':
        async with state.proxy() as data:
            await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text='Это не файл .json♻️', reply_markup=ikb_back)
            return
            
    json_cfg=await message.document.download(destination_dir='data//cash_config')
    with open(json_cfg.name, 'r') as json_file:
        data_import=json.loads(json_file.read())
    patch_logs=f'data//cash_config//log_import{str(datetime.now())}.txt'.replace(':', '.')
    file_logs_update=open(patch_logs, 'w+', encoding='UTF-8')
    async with state.proxy() as data:
        await bot.edit_message_text(chat_id=message.from_user.id, message_id=data['message_id'], text='<b>Импорт файла...</b>',parse_mode=types.ParseMode.HTML)
    if data_import.get('user_data') != None:
        for i in data_import.get('user_data'):
            try:
                data_user=[i[0], i[1], i[2], i[3]]
                cs.execute("INSERT INTO user_data VALUES(?, ?, ?, ?)", data_user)
                file_logs_update.write(f'Добавил пользователя: {i[1]}\n')
            except:
                file_logs_update.write(f'Ошибка при добавлении, пользователь: {i[1]}\n')
        file_logs_update.write('\n\n')

    if data_import.get('text_data') != None:
        for i in data_import.get('text_data'):
            cs.execute(f"UPDATE text_data SET text_text = '{i[1]}' WHERE text_type = '{i[0]}'")
            file_logs_update.write(f'Изминилл {i[0]} на: {i[1]}\n')
        file_logs_update.write('\n\n')

    if data_import.get('search_data') != None:
        for i in data_import.get('search_data'):
            data_search=[i[0], i[1]]
            try:
                cs.execute("INSERT INTO search_data VALUES(?, ?)", data_search)
                file_logs_update.write(f'Добавил истрию поиска: {i[0]}({i[1]})\n')
            except:
                file_logs_update.write(f'Не смог добавить истории поиска: {i[0]}({i[1]})\n')
        file_logs_update.write('\n\n')

    if data_import.get('player_data') != None:
        for i in data_import.get('player_data'):
            cs.execute(f"UPDATE player_data SET kb_name = '{i[3]}' WHERE player_name = '{i[1]}'")
            file_logs_update.write(f'Изминил настройки плеера: {i[0]}\n')
        file_logs_update.write('\n\n')

    if data_import.get('films_data') != None:
        for i in data_import.get('films_data'):
            try:
                data_films=[i[0], i[1], i[2]]
                cs.execute("INSERT INTO films_data VALUES(?, ?, ?)", data_films)
                file_logs_update.write(f'Добавил фильм: {i[1]}({i[0]})\n')
            except:
                file_logs_update.write(f'Ошибка при добавлении, фильма: {i[1]}({i[0]})\n')
        file_logs_update.write('\n\n')

    if data_import.get('chennel_data') != None:
        for i in data_import.get('chennel_data'):
            try:
                data_chennel=[i[0], i[1], i[2]]
                cs.execute("INSERT INTO chennel_data VALUES(?, ?, ?)", data_chennel)
                file_logs_update.write(f'Добавил канал: {i[1]}({i[0]})\n')
            except:
                file_logs_update.write(f'Ошибка при добавлении, канала: {i[1]}({i[0]})\n')
        file_logs_update.write('\n\n')

    if data_import.get('franchise_data') != None:
        for i in data_import.get('franchise_data'):
            try:
                data_franchise=[i[0], i[1]]
                cs.execute("INSERT INTO franchise_data VALUES(?, ?)", data_franchise)
                file_logs_update.write(f'Добавил объект в франшизу: {i[1]}({i[0]})\n')
            except:
                file_logs_update.write(f'Ошибка при добавлении, объект в франшизу: {i[1]}({i[0]})\n')
        file_logs_update.write('\n\n')
                
    if data_import.get('favourites_data') != None:
        counter_fav=int()
        for i in data_import.get('favourites_data'):
            data_favourites=[i[0], i[1]]
            cs.execute("INSERT INTO favourites_data VALUES(?, ?)", data_favourites)
            counter_fav+=1
        file_logs_update.write(f'Возобновил избранные, всего {counter_fav}')
    file_logs_update.close()
    sql.commit()
    async with state.proxy() as data:
        await bot.delete_message(chat_id=message.from_user.id, message_id=data['message_id'])
    await bot.send_document(chat_id=message.from_user.id, document=open(file=patch_logs, mode='rb'), caption='<b>Конфиг успешно загружен✅\nВы можете посмотреть изминение файле выше📄</b>', reply_markup=ikb_close, parse_mode=types.ParseMode.HTML)
    await state.finish()

    

#Автор: @K1p1k#
#Загружено с TG @KiTools#
#Оставь эту надпись#