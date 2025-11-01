from aiogram import Router
from bot.handlers import start, user_input

router = Router()
router.include_router(start.start_router)
router.include_router(user_input.name_router)