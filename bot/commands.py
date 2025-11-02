from aiogram.types import BotCommand

async def setup_commands(bot):
    commands = [
        BotCommand(command="start", description="Start the adventure"),
    ]
    await bot.set_my_commands(commands)