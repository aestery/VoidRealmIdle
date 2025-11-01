from asyncpg import Pool
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from core.game_objects.player import Player
from .start import NameState 

name_router = Router()

@name_router.message(NameState.waiting_for_name)
async def set_name(message: types.Message, state: FSMContext, pool: Pool):
    name: str = message.text   

    if not (1 <= len(name) <= 20):
        await message.answer("Name must be 1–20 characters. Try again:")
        return

    player = Player(pool, message.from_user.id)
    await player.set_name(name)
    await state.clear()