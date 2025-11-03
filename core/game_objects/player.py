from core.Database import PlayerTable
from core.text_handle import Language
from core.dto.responce_dto import Responce
from core.game_objects.kinds import Kind
from typing import Tuple

class Player:
    """Represents a game player; handles DB-backed operations."""
    MIN_NAME_LEN = 1
    MAX_NAME_LEN = 50

    def __init__(self, pool, user_id: int):
        self.pool = pool
        self.id = user_id
        self.playerDatabase = PlayerTable(pool, user_id)

    # --- Creation & Initialization ---
    async def create(self, name: str | None = None, language:Language=Language('en')) -> None:
        """Create new player in DB."""
        await self.playerDatabase.create_character(name, language)

    # --- Getters ---
    async def get_name(self) -> Tuple[bool, str]:
        """Fetch player name and language."""
        name = await self.playerDatabase.get_character_name()
        return (bool(name), name)
    
    async def get_language(self) -> Language:
        """Return current player language."""
        language = await self.playerDatabase.get_language()
        return Language(language)
    
    async def get_kind(self) -> Kind:
        """Return kind of player character."""
        race_str = await self.playerDatabase.get_kind()
        return Kind(race_str)
    
    # --- Setters ---
    async def set_language(self, language:Language) -> None:
        """Update player language."""
        await self.playerDatabase.set_language(language)
    
    async def set_name(self, name:str) -> bool:
        """Set name if within limits."""
        valid = self.MIN_NAME_LEN <= len(name) <= self.MAX_NAME_LEN

        if valid:
            await self.playerDatabase.set_character_name(name)
    
        return valid
    
    async def set_kind(self, kind: Kind) -> None:
        """Set player kind if not found if db."""
        kind = await self.playerDatabase.get_kind()
        if kind:
            await self.playerDatabase.set_kind(kind.value)
    
