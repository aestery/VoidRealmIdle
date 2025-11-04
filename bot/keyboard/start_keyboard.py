from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

from core.text_handle import Languages
from core.game_objects.kinds import Kind

def start_keyboard():
    kb = [
        [KeyboardButton(text="Start Adventure")],
    ]

    return ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True
    )

async def kind_choise_keyboard(message: types.Message):
    kb = InlineKeyboardMarkup(row_width=2)
    for kind in Kind:
        kb.insert(InlineKeyboardButton(text=kind.value.capitalize(), callback_data=kind.value))
    return kb

async def language_choice_keyboard(message: types.Message):
        kb = InlineKeyboardBuilder()
        kb.button(text="English", callback_data=Languages.eng)
        kb.button(text="Русский", callback_data=Languages.rus)
        kb.adjust(2)
        # Language initialization question in most recognizable and translatable language.
        await message.answer("Choose your language:", reply_markup=kb.as_markup()) 