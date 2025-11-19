import asyncpg
from core.database.Database import DatabaseTable, SCHEMA

class PlayerTable(DatabaseTable):
    def __init__(self, pool: asyncpg.Pool, user_id: int):
        super().__init__(pool)
        self.TABLE_NAME = f"{SCHEMA}.player_info"

        self.CHARACTER_NAME = "character_name"
        self.LANGUAGE = "language"
        self.KIND = "kind"

        self.user_id = user_id

    async def player_exists(self):
        async with self.pool.acquire() as connection:
            return await connection.fetchval(
                f"SELECT EXISTS ("
                f"SELECT 1 FROM {self.TABLE_NAME} "
                f"WHERE {self.KEY} = $1);",
                self.user_id
            )

    async def create_character(self, name: str, language: str) -> None:
        async with self.pool.acquire() as connection:
            status = await connection.execute(
                f"INSERT INTO {self.TABLE_NAME} "
                f"({self.KEY}, {self.CHARACTER_NAME}, {self.LANGUAGE}) "
                "VALUES ($1, $2, $3) "
                f"ON CONFLICT ({self.KEY}) DO NOTHING;",
                self.user_id, name, language
            )
            self.logger.debug("TRANSACTION_STATUS character creation: %s", status)

    async def get_character_name(self) -> str:
        return await self._get_element(key=self.user_id, attribute=self.CHARACTER_NAME)

    async def get_language(self) -> str:
        return await self._get_element(key=self.user_id, attribute=self.LANGUAGE) 

    async def get_kind(self) -> str:
        return await self._get_element(key=self.user_id, attribute=self.KIND)   

    async def set_character_name(self, name: str) -> None:
        await self._set_element(key=self.user_id, attribute=self.CHARACTER_NAME, value=name)
    
    async def set_language(self, language: str) -> None:
        await self._set_element(key=self.user_id, attribute=self.LANGUAGE, value=language)
    
    async def set_kind(self, kind: str) -> None:
        await self._set_element(key=self.user_id, attribute=self.KIND, value=kind)


class PlayerStatsDatabase(DatabaseTable):
    def __init__(self, pool: asyncpg.Pool, user_id: int):
        super().__init__(pool)
        self.TABLE_NAME = f"{SCHEMA}.player_character_stats"

        self.MAX_HEALTH = "max_health"
        self.CURRENT_HEALTH = "current_health"
        self.ATTACK = "attack"

        self.user_id = user_id
    
    async def get_max_health(self):
        await self._get_element(key=self.user_id, attribute=self.MAX_HEALTH)
    async def get_current_health(self):
        await self._get_element(key=self.user_id, attribute=self.CURRENT_HEALTH)
    async def get_attack(self): 
        await self._get_element(key=self.user_id, attribute=self.ATTACK)

    async def set_max_health(self, max_health: int):
        await self._set_element(key=self.user_id, attribute=self.MAX_HEALTH, value=max_health)
    async def set_current_health(self, current_health: int):
        await self._set_element(key=self.user_id, attribute=self.CURRENT_HEALTH, value=current_health)
    async def set_attack_value(self, attack: int):
        await self._set_element(key=self.user_id, attribute=self.ATTACK, value=attack)
    