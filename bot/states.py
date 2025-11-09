from aiogram.fsm.state import State, StatesGroup

class InitStates(StatesGroup):
    wait_for_name = State()
    wait_for_language = State()
    wait_for_kind = State()
    wait_to_end = State()

class IntroductionStates(StatesGroup):
    wait_to_start = State()