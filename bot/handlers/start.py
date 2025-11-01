import asyncpg
from aiogram import Router, types
from aiogram.filters import Command
from core.game_objects.player import Player

start_router = Router()

@start_router.message(Command("start"))
async def start(message: types.Message, pool: asyncpg.Pool):
    user_id = message.chat.id

    player = Player(pool)
    await player.create(user_id)
    data = await player.get(user_id)

    await message.answer(f"Welcome, {data['player_id']}! Strength: {data['playerstrength']}, Level: {data['playerlvl']}")