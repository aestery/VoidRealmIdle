import psycopg2
from psycopg2._psycopg import cursor
import asyncpg

PLAYER_DB = "test.player_info"

class PlayerDatabase():
    id = "user_id"
    name = "character_name"

    @staticmethod
    async def get_character_name(pool: asyncpg.Pool, user_id: int) -> str:
        async with pool.acquire() as connection:
            return await connection.fetchval(f"SELECT {PlayerDatabase.name} FROM {PLAYER_DB} WHERE {PlayerDatabase.id}={user_id}")

    @staticmethod
    async def set_character_name(pool: asyncpg.Pool, user_id: int, name: str) -> None:
        async with pool.acquire() as connection:
            await connection.execute(f"UPDATE {PLAYER_DB} " 
                                     f"SET {PlayerDatabase.name} = $2 "
                                     f"WHERE {PlayerDatabase.id} = $1; ",
                                     user_id, name)

class StatsDatabase:
    pass


class DatabaseHandle():
    def __init__(self, dataBaseURL) -> None:
        self._dataBaseURL = dataBaseURL
    
    async def create_pool(self, minConnections=1, maxConnections=10) -> asyncpg.Pool:
        return await asyncpg.create_pool(
            dsn=self._dataBaseURL,
            min_size=minConnections,
            max_size=maxConnections
        )
