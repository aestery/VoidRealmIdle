import logging
from typing import Tuple
from core.database.player import PlayerTable
from core.dto.text_dto import Language


class Player:
    """Represents a game player; handles DB-backed operations."""
    MIN_NAME_LEN = 1
    MAX_NAME_LEN = 50

    def __init__(self, pool, user_id: int):
        self.pool = pool
        self.id = user_id
        self.playerDatabase = PlayerTable(pool, user_id)
        self.logger = logging.getLogger(__name__)

    # --- Creation & Initialization ---
    async def create(self, name: str | None = None, language:Language=Language('en')) -> None:
        """Create new player in DB."""
        player_exists = await self.playerDatabase.player_exists()
        self.logger.debug("Try to create player in db, player status: %s:", str(player_exists))
        if player_exists == False:
            await self.playerDatabase.create_character(name, language)

    # --- Getters ---
    async def get_name(self) -> Tuple[bool, str]:
        """Fetch player name and language."""
        name = await self.playerDatabase.get_character_name()
        return (bool(name), name)
    
    async def get_language(self) -> Language:
        """Return current player language."""
        self.logger.debug("GET language")
        language = await self.playerDatabase.get_language()
        self.logger.debug("GOT language: %s", language)
        return Language(language)
    
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


    
