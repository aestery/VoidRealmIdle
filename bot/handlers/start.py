import asyncpg

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder, KeyboardBuilder

from core.game_objects.player import Player
from core.text_handle import Language, Languages, I18n
from bot.states import NameState, LanguageState


start_router = Router()
name_router = Router()
language_router = Router()

@start_router.message(Command("start"))
async def start(message: types.Message, state: FSMContext, pool: asyncpg.Pool) -> None:
    user_id: int = message.from_user.id 

    player = Player(pool, user_id)
    await player.create()
    
    await language_initialization(message, state)
    i18n = I18n(await player.get_language())
    name = await player.get_name()

    if name:
        await message.answer(i18n.text("welcome_back", username=name))
    else:
        await message.answer(i18n.text("welcome_new"))
        await state.set_state(NameState.waiting_for_name)

@name_router.message(NameState.waiting_for_name)
async def set_name(message: types.Message, state: FSMContext, pool: asyncpg.Pool) -> None:
    name: str = message.text
    player = Player(pool, message.from_user.id)
    language = await player.get_language()
    i18n = I18n(language)   

    if not (1 <= len(name) <= 20):
        await message.answer(i18n.text("name_invalid"))
        return

    await player.set_name(name)
    await state.clear()

async def language_initialization(message: types.Message, state: FSMContext) -> None:
    kb = InlineKeyboardBuilder()
    kb.button(text="English", callback_data=Languages.eng)
    kb.button(text="Русский", callback_data=Languages.rus)
    kb.adjust(2)
    await message.answer("Choose your language:", reply_markup=kb.as_markup())
    await state.set_state(LanguageState.waiting_for_language)

@language_router.callback_query(LanguageState.waiting_for_language)
async def set_language(callback: types.CallbackQuery, state: FSMContext, pool: asyncpg.Pool) -> None:
    language = callback.data  # 'en' or 'ru'

    player = Player(pool, callback.from_user.id)
    await player.set_language(language)
    
    i18n = I18n(language)

    await state.clear()
    await callback.message.edit_text(i18n.text("language_set"))