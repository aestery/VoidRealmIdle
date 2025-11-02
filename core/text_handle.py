import json
from typing import NewType
from core.dto.text_dto import TextDTO

Language = NewType('Language', str)

class Languages:
    eng = Language('en')
    rus = Language('ru')

# Current implementation assume existance of localization files in project folder. Usage of Database under question
class I18n:
    def __init__(self, language:Language="en"):
        with open(f"locales/{language}.json", "r", encoding="utf-8") as file:
            self.texts = TextDTO.from_dict(json.load(file))