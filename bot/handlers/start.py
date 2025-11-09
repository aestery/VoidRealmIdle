import asyncpg

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from core.text.localization import I18n
from core.text.initialization_text import InitializationTexts
from core.game_objects.player import Player
from core.dto.text_dto import Language
from bot.states import InitStates, IntroductionStates
from bot.keyboard.start_keyboard import language_choice_keyboard
from bot.handlers.base_handler import BaseHandler


class PlayerInitializationHandler(BaseHandler):
    def __init__(self):
        super().__init__()
        self.logger.debug("player object created")
    
    def _set_routers(self):
        self.start_router = Router(name="Player Initialization")
        self.language_router = Router(name="Language Initialization")
        self.name_router = Router(name="Name Initialization")
        self.end_router = Router(name="End Initialization")
    
    def _register_routers(self):
        self.start_router.message.register(self.start, Command("start"))
        self.language_router.callback_query.register(self.set_language, InitStates.wait_for_language)
        self.name_router.message.register(self.set_name, InitStates.wait_for_name)
        self.end_router.callback_query.register(self.end, InitStates.wait_to_end)

    async def start(self, message: types.Message, state: FSMContext, pool: asyncpg.Pool, i18n: I18n) -> None:
        """Initialization of player in database"""
        self.logger.debug("player creation step started")
        user_id: int = message.from_user.id 

        self.player = Player(pool, user_id)
        self.text_handler: InitializationTexts = InitializationTexts(i18n)
        await self.player.create()
        
        await language_choice_keyboard(message)
        await state.set_state(InitStates.wait_for_language)
        self.logger.debug("player creation step ended")

    async def set_language(self, callback: types.CallbackQuery, state: FSMContext, i18n: I18n) -> None:
        """Set up game language for convenient experience"""
        language: Language = callback.data
        await self.player.set_language(language)
        i18n.set_actual_language(language)

        await state.clear()
        await callback.message.edit_text(self.text_handler.language_setup_message())

        await self.name_initialization(callback.message, state)

    async def name_initialization(self, message: types.Message, state: FSMContext):
        has_name, name = await self.player.get_name()

        if has_name:
            await message.answer(self.text_handler.welcome_existing_player(name))
            await state.set_state(InitStates.wait_to_end)
        else:
            await message.answer(self.text_handler.welcome_new_player())
            await state.set_state(InitStates.wait_for_name)

    async def set_name(self, message: types.Message, state: FSMContext, pool: asyncpg.Pool) -> None:
        """Set up character name"""
        name: str = message.text
        is_valid_name = await self.player.set_name(name)
        language = await self.player.get_language()
        i18n = I18n(language)   

        if not is_valid_name:
            await message.answer(self.text_handler.name_invalid())
            return
        else:
            await message.answer(self.text_handler.name_valid(name))

        await state.clear()
        await state.set_state(InitStates.wait_to_end)
    
    async def end(self, callback: types.CallbackQuery, state: FSMContext, pool: asyncpg.Pool):
        await state.clear()
        await state.set_state(IntroductionStates.wait_to_start)


class IntroductionLevel(BaseHandler):
    def __init__(self):
        super().__init__()
        self.logger.debug("Education level started")

    def _set_routers(self):
        self.start_router = Router()
    
    def _register_routers(self):
        self.start_router.callback_query.register(self.start, IntroductionStates.wait_to_start)

    async def start(self, callback: types.CallbackQuery, state: FSMContext, pool: asyncpg.Pool):
        self.pool = pool
        self.player = Player(pool=pool, user_id=callback.message.from_user.id)
        
    async def end(self, callback: types.CallbackQuery, state: FSMContext, pool: asyncpg.Pool):
        pass