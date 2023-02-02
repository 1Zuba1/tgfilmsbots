from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from data.db import only_list, get_AllFilms, get_dataUser

class IsCode(BoundFilter):
    async def check(self, message: types.Message):
        data_code=await only_list(await get_AllFilms(type='films_code'))
        for i in data_code:
            if i == message.text:
                return True
        return False

class IsinFavourites(BoundFilter):
    async def check(self, call: types.CallbackQuery):
        return True if call.data[0:14] == 'in_favourites_' else False

class IsDeleteFavourites(BoundFilter):
    async def check(self, call: types.CallbackQuery):
        return True if call.data[0:18] == 'delete_favourites_' else False

class IsSearchWCall(BoundFilter):
    async def check(self, call: types.CallbackQuery):
        return True if call.data[0:12] == 'search_film_' else False
