from dataclasses import dataclass
from typing import Any
from core.game_objects.kinds import Kind

@dataclass
class Responce:
    status: bool
    value: Any = None
