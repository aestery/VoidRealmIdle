from dataclasses import dataclass
from core.text_handle import Language

@dataclass
class Responce():
    status: bool

@dataclass
class StringResponce(Responce):
    value: str
