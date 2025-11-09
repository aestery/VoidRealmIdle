import yaml
import asyncio
import logging
import logging.config
from asyncpg import Pool
from decouple import config
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from bot.router import router
from bot.commands import setup_commands
from bot.logging.logger_handler import LoggingMiddleware
from core.Database import DatabaseHandle
from core.text.localization import I18n


# Run the bot
async def main() -> None:
    dataBase = DatabaseHandle(config('DB_URL'))

    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    admins = [int(admin_id) for admin_id in config('ADMINS', cast=str).split(',')] #type: ignore

    with open(config('MIDDLEWARE_LOG_CONFIG'), "r") as f:
        log_config = yaml.safe_load(f.read())
        logging.config.dictConfig(log_config)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.info("Logging initialized")

    bot = Bot(
        token=config('TOKEN', cast=str),  # type: ignore
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    i18n = I18n(config('LOCALES'))
    databasePool:Pool = await dataBase.create_pool()

    dispatcher = Dispatcher(
        storage=MemoryStorage(), 
        pool=databasePool, 
        i18n=i18n
    )
    dispatcher.message.middleware(LoggingMiddleware(logger))
    
    dispatcher.callback_query.middleware(LoggingMiddleware(logger))
    dispatcher.include_router(router)

    await setup_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

