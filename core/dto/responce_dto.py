from typing import TypedDict, NotRequired
from core.game_objects.kinds import Kind


class Responce(TypedDict):
    status: bool
    value: NotRequired[str | Kind]
