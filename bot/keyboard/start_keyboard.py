from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
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

def kind_choise_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)
    for kind in Kind:
        kb.insert(InlineKeyboardButton(text=kind.value.capitalize(), callback_data=kind.value))
    return kb