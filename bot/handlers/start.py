import asyncpg
import inspect

from aiogram import Router, types
from aiogram.filters import Command, F
from aiogram.fsm.context import FSMContext

from core.game_objects.player import Player
from core.text_handle import I18n
from bot.states import InitStates
from bot.keyboard.start_keyboard import language_choice_keyboard


class BaseHandler:
    """
    Base handler class that automatically builds a composite router
    from all attributes ending with '_router'.
    """
    def __init__(self):
        self.router = Router(name=self.__class__.__name__)
    
    def get_class_router(self):
        """
        Finds all attributes ending with '_router' and includes them
        into the main router.
        """
        for name, attr in inspect.getmembers(self):
            if name.endswith("_router") and isinstance(attr, Router):
                self.router.include_router(attr)
        
        return self.router

class PlayerInitializationHandler(BaseHandler):
    def __init__(self):
        super().__init__()
        self.player: Player = None

        self.start_router = Router(name="Player Initialization")
        self.language_router = Router(name="Language Initialization")
        self.name_router = Router(name="Name Initialization")
        self.kind_router = Router(name="Kind Initialization")

        self.start_router.message.register(self.start, Command("start"))
        self.language_router.message.register(self.set_language, InitStates.waiting_for_language)
        self.name_router.message.register(self.set_name, InitStates.waiting_for_name)
        self.kind_router.message.register(self.set_kind, InitStates.waiting_for_kind)

    async def start(self, message: types.Message, state: FSMContext, pool: asyncpg.Pool) -> None:
        """Initialization of player in database"""
        user_id: int = message.from_user.id 

        self.player = Player(pool, user_id)
        await self.player.create()
        
        await language_choice_keyboard(message)
        await state.set_state(InitStates.waiting_for_language)

    async def set_language(self, callback: types.CallbackQuery, state: FSMContext, pool: asyncpg.Pool) -> None:
        """Set up game language for convenient experience"""
        language = callback.data  # 'en' or 'ru'
        await self.player.set_language(language)
        
        i18n = I18n(language)

        await state.clear()
        await callback.message.edit_text(i18n.texts.start.messages_text.language_set)

        await self.name_initialization(callback.message, state, self.player)

    async def name_initialization(message: types.Message, state: FSMContext, player: Player):
        has_name, name = await player.get_name()
        language = await player.get_language()
        i18n = I18n(language)   

        if has_name:
            await message.answer(i18n.texts.start.messages_text.welcome_back.format(username=name))
            await state.set_state(InitStates.waiting_for_kind)
        else:
            await message.answer(i18n.texts.start.messages_text.welcome_new)
            await state.set_state(InitStates.waiting_for_name)

    async def set_name(message: types.Message, state: FSMContext, pool: asyncpg.Pool) -> None:
        """Set up character name"""
        name: str = message.text
        player = Player(pool, message.from_user.id)
        is_valid_name = await player.set_name(name)
        language = await player.get_language()
        i18n = I18n(language)   

        if not is_valid_name:
            await message.answer(i18n.texts.start.messages_text.name_invalid)
            return
        else:
            await message.answer(i18n.texts.start.messages_text.name_valid.format(username=name))

        await state.clear()
        await state.set_state(InitStates.waiting_for_kind)

    async def set_kind(message: types.Message, state: FSMContext, pool: asyncpg.Pool):
        pass