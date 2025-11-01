from aiogram import Router
from bot.handlers import start

router = Router()
router.include_router(start.start_router)
router.include_router(start.name_router)
router.include_router(start.language_router)