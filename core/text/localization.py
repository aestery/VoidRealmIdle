import os
import json
import logging
from typing import Dict, Any

from core.dto.text_dto import Language, Languages, LocaleDTO


class I18n:
    """
    I18n system backed by Pydantic DTOs for locales.

    - Loads each JSON locale file into a strongly-typed `LocaleDTO`.
    - Exposes attribute-based access via `i18n.current` (e.g. `i18n.current.messages_text.start.welcome_new_player`).
    - Keeps `get_text(key: str)` for compatibility, implemented on top of the DTO tree.
    """

    def __init__(self, locales_dir: str):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("LOAD locale texts")

        # lang code (e.g. "en", "ru") -> LocaleDTO
        self._locale_models: Dict[str, LocaleDTO] = self._load_all_locales(locales_dir)

        self.default_lang: Language = Languages.eng
        self.actual_language: Language | None = None

    def _load_all_locales(self, path: str) -> Dict[str, LocaleDTO]:
        """
        Load all locale JSON files and validate them via Pydantic DTOs.
        """
        models: Dict[str, LocaleDTO] = {}

        for filename in os.listdir(path):
            if not filename.endswith(".json"):
                continue

            lang = filename.split(".")[0]
            full_path = os.path.join(path, filename)

            with open(full_path, "r", encoding="utf-8") as file:
                raw_data = json.load(file)

            try:
                locale_model = LocaleDTO.model_validate(raw_data)
            except Exception as exc:
                self.logger.error("Failed to load locale '%s': %s", lang, exc)
                raise

            models[lang] = locale_model

        return models

    def _get_current_model(self) -> LocaleDTO:
        """
        Return the LocaleDTO for the current (or default) language.
        """
        language: Language = self.actual_language if self.actual_language is not None else self.default_lang
        lang_key = str(language)

        model = self._locale_models.get(lang_key)
        if model is None and lang_key != str(self.default_lang):
            # Fallback to default language if missing
            self.logger.warning("Locale '%s' not found, falling back to default '%s'", lang_key, self.default_lang)
            model = self._locale_models.get(str(self.default_lang))

        if model is None:
            raise RuntimeError("No locale models loaded; cannot resolve texts")

        return model

    @property
    def current(self) -> LocaleDTO:
        """
        Currently active locale model for attribute-based access.

        Example:
            i18n.current.messages_text.start.welcome_new_player
        """
        return self._get_current_model()

    def set_actual_language(self, language: str | None) -> None:
        """
        Set current language (falls back to default if None).
        """
        if not language:
            language = Languages.eng
        self.logger.debug("Language changed to %s", str(language))
        self.actual_language = Language(language)

    def get_text(self, key: str) -> str:
        """
        Fetch localized text by dotted key using the DTO tree
        (e.g. 'messages_text.start.welcome_new_player').
        """
        model: Any = self._get_current_model()

        value: Any = model
        for part in key.split("."):
            if hasattr(value, part):
                value = getattr(value, part)
            elif isinstance(value, dict) and part in value:
                value = value[part]
            else:
                self.logger.warning("Key part '%s' not found while resolving '%s'", part, key)
                return ""

        return str(value)