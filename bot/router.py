from aiogram import Router
from bot.handlers.base_handler import BaseHandler
from bot.handlers.start import PlayerInitializationHandler
from bot.handlers.menu import Menu


router = Router()

# Seems like here would be contained all game stages. Somehow it feels incorrect.
handlers: list[BaseHandler] = [
    PlayerInitializationHandler(),
    Menu()
]

# Set up router hierarchy 
for handler in handlers:
    router.include_router(handler.get_class_router())


