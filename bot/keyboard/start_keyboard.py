from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def start_keyboard():
    kb = [
        [KeyboardButton(text="Start Adventure")],
    ]

    return ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True
    )