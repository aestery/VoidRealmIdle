from core.Database import PlayerDatabase
from core.text_handle import Language

class Player:
    def __init__(self, pool, user_id):
        self.pool = pool
        self.id = user_id

    async def create(self, name:str=None, language:Language=Language('en')):
        await PlayerDatabase.create_character(self.pool, self.id, name, language)
    
    async def get_name(self) -> str:
        return await PlayerDatabase.get_character_name(self.pool, self.id)
    
    async def set_name(self, name:str) -> None:
        return await PlayerDatabase.set_character_name(self.pool, self.id, name)
    
    async def set_language(self, language:Language) -> None:
        await PlayerDatabase.set_language(self.pool, self.id, language)
    
    async def get_language(self) -> Language:
        return await Language(PlayerDatabase.get_language(self.pool, self.id))
    
