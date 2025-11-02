import asyncpg

from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.game_objects.player import Player
from core.text_handle import Languages, I18n, TextKeys
from bot.states import NameState, LanguageState


start_router = Router()
name_router = Router()
language_router = Router()

@start_router.message(Command("start"))
async def start(message: types.Message, state: FSMContext, pool: asyncpg.Pool) -> None:
    """Initialization of player in database"""
    user_id: int = message.from_user.id 

    player = Player(pool, user_id)
    await player.create()
    
    await language_initialization(message, state)

async def language_initialization(message: types.Message, state: FSMContext) -> None:
    kb = InlineKeyboardBuilder()
    kb.button(text="English", callback_data=Languages.eng)
    kb.button(text="Русский", callback_data=Languages.rus)
    kb.adjust(2)
    await message.answer("Choose your language:", reply_markup=kb.as_markup()) # Initial question in most recognizable and translatable language.
    await state.set_state(LanguageState.waiting_for_language)

@language_router.callback_query(LanguageState.waiting_for_language)
async def set_language(callback: types.CallbackQuery, state: FSMContext, pool: asyncpg.Pool) -> None:
    """Set up game language for convenient experience"""
    language = callback.data  # 'en' or 'ru'

    player = Player(pool, callback.from_user.id)
    await player.set_language(language)
    
    i18n = I18n(language)

    await state.clear()
    await callback.message.edit_text(i18n.text(TextKeys.language_set))

    await name_initialization(callback.message, state, player)

async def name_initialization(message: types.Message, state: FSMContext, player: Player):
    responce = await player.get_name()
    language = await player.get_language()
    i18n = I18n(language)   

    if responce.status:
        await message.answer(i18n.text(TextKeys.welcome_back, username=responce.value))
    else:
        await message.answer(i18n.text(TextKeys.welcome_new))
        await state.set_state(NameState.waiting_for_name)

@name_router.message(NameState.waiting_for_name)
async def set_name(message: types.Message, state: FSMContext, pool: asyncpg.Pool) -> None:
    """Set up character name"""
    name: str = message.text
    player = Player(pool, message.from_user.id)
    responce = await player.set_name(name)
    language = await player.get_language()
    i18n = I18n(language)   

    if not responce.status:
        await message.answer(i18n.text(TextKeys.name_invalid))
        return
    else:
        await message.answer(i18n.text(TextKeys.name_valid))

    await state.clear()

