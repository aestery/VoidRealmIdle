from aiogram.types import BotCommand

# Centrilized command definition. Might be redundant. Probably would not use commands or would use it the other way.
async def setup_commands(bot):
    commands = [
        BotCommand(command="start", description="Start the adventure"),
    ]
    await bot.set_my_commands(commands)