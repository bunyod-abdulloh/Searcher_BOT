from aiogram.filters.state import StatesGroup, State


class SearchAllUz(StatesGroup):
    Q1 = State()


class AdminState(StatesGroup):
    are_you_sure = State()
    ask_ad_content = State()
