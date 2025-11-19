from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from core.dto.text_dto import Languages

class MenuKeyboard:
    ENTER_MENU_BUTTON = "Menu"
    
    @classmethod
    def enter_menue_keyboard(cls) -> ReplyKeyboardMarkup:
        kb = ReplyKeyboardBuilder()
        kb.button(text=cls.ENTER_MENU_BUTTON)
        return kb.as_markup()

class PlayerInitializationKeyboard:
    @classmethod
    async def language_choice_keyboard(cls) -> InlineKeyboardMarkup:
            kb = InlineKeyboardBuilder()
            kb.button(text="English", callback_data=Languages.eng)
            kb.button(text="Русский", callback_data=Languages.rus)
            kb.adjust(2)
            return kb.as_markup()
