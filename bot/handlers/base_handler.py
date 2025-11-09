import inspect
import logging
import asyncpg
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from abc import ABC, abstractmethod

from core.game_objects.player import Player
from core.text.base_text_access import BaseTextAcess


class ICallbackHandler(ABC):
    @abstractmethod
    async def start(self, callback: types.CallbackQuery, pool: asyncpg.Pool, state: FSMContext):
        """entry point to game substage, should be defined with """
    @abstractmethod
    async def end(self, callback: types.CallbackQuery, pool: asyncpg.Pool, state: FSMContext):
        """exit point, defines followup interactions"""
    @abstractmethod
    def _set_routers(self):
        """define aiogram routers of handler"""
    @abstractmethod
    def _register_routers(self):
        """register defined routers"""


class BaseHandler(ICallbackHandler):
    """
    Base handler class that automatically builds a composite router
    from all attributes ending with '_router'.
    """
    def __init__(self):
        self.router = Router(name=self.__class__.__name__)
        self.logger = logging.getLogger(name = f"{self.__class__.__module__}.{self.__class__.__name__}")

        self.player: Player | None = None
        self.text_handler: BaseTextAcess | None = None

        self._set_routers()
        self._register_routers()

    def get_class_router(self):
        """
        Finds all attributes ending with '_router' and includes them
        into the main router.
        """
        for name, attr in inspect.getmembers(self):
            if name.endswith("_router") and isinstance(attr, Router):
                self.router.include_router(attr)

        self.logger.debug("Handler formed super router: %s", self.router.name)
        return self.router
