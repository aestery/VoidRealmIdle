from aiogram import Router
from bot.handlers import start
from bot.handlers.start import PlayerInitializationHandler


router = Router()

player_initialization = PlayerInitializationHandler()
router.include_router(player_initialization.get_class_router())

