from dataclasses import dataclass

@dataclass
class Responce():
    status: bool

@dataclass
class StringResponce(Responce):
    value: str
