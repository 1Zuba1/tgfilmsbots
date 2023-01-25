#by @K1p1k#
#Downloaded from TG @KiTools#
#Leave this inscription#

from aiogram.dispatcher.filters.state import State, StatesGroup

#состояние админа#
class Admin_State(StatesGroup):
    class add_film(StatesGroup):
        code=State()
        name=State()
        priew=State()
    class myling_list(StatesGroup):
        text=State()
    class delete_film(StatesGroup):
        code=State()
    class add_chennel(StatesGroup):
        username=State()
        link=State()
    class add_franchise(StatesGroup):
        name_obj=State()
        description=State()
    class delete_franchise(StatesGroup):
        name_obj=State()
    class delete_chennel(StatesGroup):
        username=State()
    class chennger_kbname_player(StatesGroup):
        text=State()
    class chennger_wellcome_text(StatesGroup):
        text=State()
    class chennger_film_text(StatesGroup):
        text=State()
    class chennger_franchise_text(StatesGroup):
        text=State()
    class import_cfg(StatesGroup):
        file=State()


#Автор: @K1p1k#
#Загружено с TG @KiTools#
#Оставь эту надпись#