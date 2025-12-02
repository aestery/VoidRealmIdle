from aiogram import F, Router, types
from aiogram.fsm.state import State, StatesGroup
from bot.handlers.base_handler import BaseHandler
from bot.keyboard.keyboard import MenuKeyboard


class MenuStates(StatesGroup):
    MENUE = State()

class Menu(BaseHandler):
    def __init__(self):
        super().__init__()
        self.logger.debug("INITIALIZE menue handler")
    
    def _set_routers(self):
        self.menue_router = Router(name="Menu")
    
    def _register_routers(self):
        self.menue_router.message.register(self.start, MenuStates.MENUE, F.text == MenuKeyboard.ENTER_MENU_BUTTON )
    
    async def start(self, message: types.Message):
        await message.answer("Welcome to menue")
