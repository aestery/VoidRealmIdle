from core.Database import PlayerDatabase
from core.text_handle import Language
from core.responce_dto import StringResponce, Responce

class Player:
    """Represents a game player; handles DB-backed operations."""
    MIN_NAME_LEN = 1
    MAX_NAME_LEN = 50

    def __init__(self, pool, user_id: int):
        self.pool = pool
        self.id = user_id

    # --- Creation & Initialization ---
    async def create(self, name: str | None = None, language:Language=Language('en')):
        """Create new player in DB."""
        await PlayerDatabase.create_character(self.pool, self.id, name, language)

    # --- Getters / Setters ---
    async def get_name(self) -> StringResponce:
        """Fetch player name and language."""
        name = await PlayerDatabase.get_character_name(self.pool, self.id)
        return StringResponce(status=bool(name), value=name)
    
    async def set_name(self, name:str) -> Responce:
        """Set name if within limits."""
        valid = self.MIN_NAME_LEN <= len(name) <= self.MAX_NAME_LEN

        if valid:
            await PlayerDatabase.set_character_name(self.pool, self.id, name)
    
        return Responce(status=valid)
    
    async def set_language(self, language:Language) -> None:
        """Update player language."""
        await PlayerDatabase.set_language(self.pool, self.id, language)
    
    async def get_language(self) -> Language:
        """Return current player language."""
        language = await PlayerDatabase.get_language(self.pool, self.id)
        return Language(language)
    
