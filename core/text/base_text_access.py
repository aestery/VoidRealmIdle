from core.text.localization import I18n


# Redundant for current version
class BaseTextAcess:
    """Base for intermediate between i18n loader and API text input"""
    def __init__(self, i18n: I18n):
        self._i18n = i18n

