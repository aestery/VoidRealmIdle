from core.text.base_text_access import BaseTextAcess
from core.text.localization import I18n


class BattleKeyboard(BaseTextAcess):
    def __init__(self, i18n: I18n):
        super().__init__(i18n)
        self._level_key = "keyboard_text.battle"
    
    def attack_choice(self) -> str: 
        return self._i18n.get_text(f"{self._level_key}.attack_choice")