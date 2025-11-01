from aiogram.fsm.state import State, StatesGroup

class NameState(StatesGroup):
    waiting_for_name = State()

class LanguageState(StatesGroup):
    waiting_for_language = State()