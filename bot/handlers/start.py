import asyncpg
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from core.game_objects.player import Player
from bot.states import NameState


start_router = Router()

@start_router.message(Command("start"))
async def start(message: types.Message, state: FSMContext, pool: asyncpg.Pool):
    user_id: int = message.from_user.id 

    player = Player(pool, user_id)
    await player.create()
    name = await player.get_name()
    
    if name:
        await message.answer(f"Welcome, {name}")
    else:
        await message.answer("Welcome, adventurer! Enter your character name (1–20 chars):")
        await state.set_state(NameState.waiting_for_name)