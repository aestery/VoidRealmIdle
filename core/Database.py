import asyncpg


SCHEMA = "test"

class DatabaseTable:
    def __init__(self, pool: asyncpg.Pool) -> None:
        self.pool = pool
        self.TABLE_NAME: str = ""
        self.KEY: str = ""

    async def _get_element(self, key: int, attribute: str):
        """
        Retrieve a single column value from the database for a given record.

        Args:
            key (int): The primary key identifying the record.
            attribute (str): The column name to retrieve.

        Returns:
            element (Any): The value of the specified column for the given key.
        """
        async with self.pool.acquire() as connection:
            return await connection.fetchval(
                f"SELECT {attribute} "
                f"FROM {self.TABLE_NAME} "
                f"WHERE {self.KEY}=$1;",
                key
            )
    
    async def _set_element(self, key: int, attribute: str, value) -> None:
        """
        Update a single column value in the database for a given record.

        Args:
            key (int): The primary key identifying the record.
            attribute (str): The column name to update.
            value (Any): The new value to assign to the column.

        Returns:
            None
        """
        async with self.pool.acquire() as connection:
            await connection.execute(
                f"UPDATE {self.TABLE_NAME} " 
                f"SET {attribute} = $1 "
                f"WHERE {self.KEY} = $2; ",
                value, key
            )

class PlayerTable(DatabaseTable):
    def __init__(self, pool: asyncpg.Pool, user_id: int):
        self.TABLE_NAME = f"{SCHEMA}.player_info"
        self.KEY = "user_id"

        self.CHARACTER_NAME = "character_name"
        self.LANGUAGE = "language"
        self.KIND = "kind"

        self.pool = pool
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
            await connection.execute(
                f"INSERT INTO {self.TABLE_NAME} "
                f"({self.KEY}, {self.CHARACTER_NAME}, {self.LANGUAGE}) "
                "VALUES ($1, $2, $3) "
                f"ON CONFLICT ({self.KEY}) DO NOTHING;",
                self.user_id, name, language
            )

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
