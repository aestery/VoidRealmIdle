from core.text.localization import I18n
from core.text.base_text_access import BaseTextAcess
from core.dto.text_dto import Language


class InitializationTexts(BaseTextAcess):
    """formatting and preparation layer for text for player initialization stage"""
    def __init__(self, i18n: I18n):
        super().__init__(i18n)

    def language_setup_message(self) -> str: 
        return self._i18n.current.messages_text.start.language_set
    def welcome_new_player(self) -> str: 
        return self._i18n.current.messages_text.start.welcome_new_player
    def welcome_existing_player(self, username: str) -> str: 
        return self._i18n.current.messages_text.start.welcome_back.format(username=username)
    def name_invalid(self) -> str: 
        return self._i18n.current.messages_text.start.name_invalid
    def name_valid(self, username: str) -> str: 
        return self._i18n.current.messages_text.start.name_valid.format(username=username)