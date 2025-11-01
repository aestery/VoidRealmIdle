import asyncpg
from core.text_handle import Language


SCHEMA = "test"

class PlayerDatabase():
    TABLE = f"{SCHEMA}.player_info"
    id = "user_id"
    character_name = "character_name"
    language = "language"

    @staticmethod
    async def get_character_name(pool: asyncpg.Pool, user_id: int) -> str:
        async with pool.acquire() as connection:
            return await connection.fetchval(
                f"SELECT {PlayerDatabase.character_name} "
                f"FROM {PlayerDatabase.TABLE} "
                f"WHERE {PlayerDatabase.id}=$1",
                user_id
            )

    @staticmethod
    async def set_character_name(pool: asyncpg.Pool, user_id: int, name: str) -> None:
        async with pool.acquire() as connection:
            await connection.execute(
                f"UPDATE {PlayerDatabase.TABLE} " 
                f"SET {PlayerDatabase.character_name} = $2 "
                f"WHERE {PlayerDatabase.id} = $1; ",
                user_id, name
            )
    
    @staticmethod
    async def create_character(pool: asyncpg.Pool, user_id: int, name: str, language: Language) -> None:
        async with pool.acquire() as connection:
            await connection.execute(
                f"INSERT INTO {PlayerDatabase.TABLE} VALUES ($1, $2, $3) "
                f"ON CONFLICT ({PlayerDatabase.id}) DO NOTHING;",
                user_id, name, language
            )
    
    @staticmethod
    async def set_language(pool: asyncpg.Pool, user_id: int, language: Language) -> None:
        async with pool.acquire() as connection:
            await connection.execute(
                f"UPDATE {PlayerDatabase.TABLE} "
                f"SET {PlayerDatabase.language}=$1 "
                f"WHERE {PlayerDatabase.id}=$2;",
                language, user_id
            )
    
    @staticmethod
    async def get_language(pool: asyncpg.Pool, user_id: int) -> str:
        async with pool.acquire() as connection:
            return await connection.fetchval(
                f"SELECT {PlayerDatabase.language} "
                f"FROM {PlayerDatabase.TABLE} "
                f"WHERE {PlayerDatabase.id}=$1;",
                user_id
            )

class PlayerStatsDatabase:
    TABLE = f"{SCHEMA}.player_stats"
    id = "user_id"

    health = ""


class DatabaseHandle():
    def __init__(self, dataBaseURL) -> None:
        self._dataBaseURL = dataBaseURL
    
    async def create_pool(self, minConnections=1, maxConnections=10) -> asyncpg.Pool:
        return await asyncpg.create_pool(
            dsn=self._dataBaseURL,
            min_size=minConnections,
            max_size=maxConnections
        )
