from asyncpg import Pool
from core.database.player import PlayerStatsDatabase


class PlayerCaracter:
    def __init__(self, pool: Pool, user_id: int):
        self.pool = pool
        self.playerId = user_id
        self.playerCaracterDatabase = PlayerStatsDatabase(self.pool, self.playerId)

        self.max_health: int = 1
        self.current_health: int = 1
        self.damage: int = 1
    
    @property
    def attack(self) -> int: 
        return self.damage
    @property
    def is_dead(self) -> bool:
        return self.current_health > 0
    
    @classmethod
    async def create(cls, pool: Pool, user_id: int):
        self = cls(pool, user_id)
        await self._set_up_stats()
        return self

    def take_damage(self, damage: int) -> None:
        self.current_health -= damage

    async def _set_up_stats(self):
        self.max_health = await self.playerCaracterDatabase.get_max_health()
        self.current_health = await self.playerCaracterDatabase.get_current_health()
        self.damage = await self.playerCaracterDatabase.get_attack()
