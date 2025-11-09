import os
import json
import logging
from core.dto.text_dto import Language, Languages


# Preload jsons and hold texts
class I18n:
    def __init__(self, locales_dir: str):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("LOAD locale texts")

        self.locales = self._load_all_locales(locales_dir)
        self.default_lang = Languages.eng
        self.actual_language = None

    def _flatten(self, data: dict, parent_key=""):
        items = {}
        for k, v in data.items():
            new_key = f"{parent_key}.{k}" if parent_key else k
            if isinstance(v, dict):
                items.update(self._flatten(v, new_key))
            else:
                items[new_key] = v
        return items

    def _load_all_locales(self, path: str):
        locales = {}
        for filename in os.listdir(path):
            if filename.endswith(".json"):
                lang = filename.split(".")[0]
                with open(os.path.join(path, filename), "r", encoding="utf-8") as file:
                    data = json.load(file)
                    locales[lang] = self._flatten(data)
        return locales
    
    def set_actual_language(self, language: Language | None) -> None:
        self.logger.debug("Language language changed to %s", str(language))
        self.actual_language = language

    def get_text(self, key: str) -> str:
        language: Language = self.actual_language if self.actual_language is not None else self.default_lang
        text = self.locales.get(str(language), None).get(key, None)
        self.logger.debug(f"{self.locales.get(language, None)}")
        if not text: 
            self.logger.warning(
                "Text with key: [%s] "
                "for language: [%s] " \
                "was not fetched from dictionary. " \
                "Final text: [%s]", 
                str(key), str(language), str(text)
                )
        
        return text