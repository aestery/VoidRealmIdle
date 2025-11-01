from core.Database import PlayerDatabase, PLAYER_DB

class Player:
    def __init__(self, pool, user_id):
        self.pool = pool
        self.id = user_id

    async def create(self, name=None):
        async with self.pool.acquire() as conn:
            await conn.execute(
                f"INSERT INTO {PLAYER_DB} VALUES ($1, $2) "
                f"ON CONFLICT ({PlayerDatabase.id}) DO NOTHING;",
                self.id, name
            )
    
    async def get_name(self) -> str:
        return await PlayerDatabase.get_character_name(self.pool, self.id)
    
    async def set_name(self, name:str) -> None:
        return await PlayerDatabase.set_character_name(self.pool, self.id, name)
    
