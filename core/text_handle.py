import json
from typing import NewType

Language = NewType('Language', str)

class Languages:
    eng = Language('en')
    rus = Language('ru')

class TextKeys:
    welcome_new = 'welcome_new'
    welcome_back = 'welcome_back'
    name_invalid = 'name_invalid'
    language_set = 'language_set'
    name_valid = 'name_valid'

# Current implementation assume existance of localization files in project folder. Usage of Database under question
class I18n:
    def __init__(self, language:Language="en"):
        with open(f"locales/{language}.json", "r", encoding="utf-8") as file:
            self.texts = json.load(file)

    def text(self, key: str, **kwargs) -> str:
        return self.texts.get(key, key).format(**kwargs)