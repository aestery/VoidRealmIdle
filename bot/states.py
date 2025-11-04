from aiogram.fsm.state import State, StatesGroup

class InitStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_language = State()
    waiting_for_kind = State()