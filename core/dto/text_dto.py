from typing import NewType
from pydantic import BaseModel


# --- Language type & available languages ---
Language = NewType("Language", str)


class Languages:
    eng: Language = Language("en")
    rus: Language = Language("ru")


# --- Pydantic DTOs describing locales JSON structure ---

class StartMessages(BaseModel):
    welcome_new_player: str
    welcome_back: str
    name_invalid: str
    name_valid: str
    language_set: str


class MessagesText(BaseModel):
    start: StartMessages


class StartKeyboardText(BaseModel):
    start: str


class BattleKeyboardText(BaseModel):
    attack_choice: str


class KeyboardText(BaseModel):
    start: StartKeyboardText
    battle: BattleKeyboardText


class LocaleDTO(BaseModel):
    """
    DTO representing a single locale JSON file (e.g. en.json, ru.json).
    """

    messages_text: MessagesText
    keyboard_text: KeyboardText