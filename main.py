import asyncio
import logging
from asyncpg import Pool
from decouple import config
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from bot.router import router
from core.Database import DatabaseHandle


dataBase = DatabaseHandle(config('DB_URL'))

scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
admins = [int(admin_id) for admin_id in config('ADMINS', cast=str).split(',')] #type: ignore

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bot = Bot(token=config('TOKEN', cast=str), default=DefaultBotProperties(parse_mode=ParseMode.HTML)) #type: ignore

# Run the bot
async def main() -> None:
    databasePool:Pool = await dataBase.create_pool()
    dispatcher = Dispatcher(storage=MemoryStorage(), pool=databasePool)
    dispatcher.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

