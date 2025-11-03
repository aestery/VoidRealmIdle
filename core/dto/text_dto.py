from typing import Any, Dict, Type, TypeVar


T = TypeVar("T", bound="JsonDTO")

class JsonDTO():
    """Base class for JSON-based DTOs."""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_dict(self) -> Dict[str, Any]:
        """Convert object (recursively) to dict."""
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, JsonDTO):
                result[key] = value.to_dict()
            else:
                result[key] = value
        return result

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        """Create DTO from dict (recursively)."""
        return cls(**{
            k: (v if not isinstance(v, dict) else JsonDTO.from_dict(v))
            for k, v in data.items()
        })

class StartMessages(JsonDTO):
    welcome_new: str
    welcome_back: str
    name_invalid: str
    name_valid: str 
    language_set: str

class StartKeyboardText(JsonDTO):
    start: str

class Start(JsonDTO):

    message_text: StartMessages
    keyboard_text: StartKeyboardText

class TextDTO(JsonDTO):
    start: Start