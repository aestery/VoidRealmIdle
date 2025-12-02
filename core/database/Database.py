import asyncpg
import logging
import inspect

#defines work schema in db
SCHEMA = "test"

class DatabaseTable:
    """
    Defines base database interaction and data.

    Predefined fields:
        logger: object in charge of action logging
        pool: object to connect database
        TABLE NAME: need to be overridden in according to expected 
    """
    def __init__(self, pool: asyncpg.Pool) -> None:
        """
        Class desctiption
        """
        self.logger = logging.getLogger(name = f"{self.__class__.__module__}.{self.__class__.__name__}")
        self.pool = pool
        self.TABLE_NAME: str = ""
        self.KEY: str = "user_id"

    async def _get_element(self, key: int, attribute: str):
        """
        Retrieve a single column value from the database for a given record.

        Args:
            key (int): The primary key identifying the record.
            attribute (str): The column name to retrieve.

        Returns:
            element (Any): The value of the specified column for the given key.
        """
        self.logger.debug("DATABASE_GET %s attribute from %s for user_id=%i", attribute, self.TABLE_NAME, key)
        async with self.pool.acquire() as connection:
            return await connection.fetchval(
                f"""SELECT {attribute} 
                    FROM {self.TABLE_NAME} 
                    WHERE {self.KEY} = $1;""",
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
        self.logger.debug("DATABASE_SET %s attribute in %s for user_id=%i with value [%s]", attribute, self.TABLE_NAME, key, str(value))
        async with self.pool.acquire() as connection:
            await connection.execute(
                f"""UPDATE {self.TABLE_NAME} 
                    SET {attribute} = $1 
                    WHERE {self.KEY} = $2;""",
                value, key
            )

class DatabaseHandle():
    def __init__(self, dataBaseURL) -> None:
        self._dataBaseURL = dataBaseURL
    
    async def create_pool(self, minConnections=1, maxConnections=10) -> asyncpg.Pool:
        return await asyncpg.create_pool(
            dsn=self._dataBaseURL,
            min_size=minConnections,
            max_size=maxConnections
        )
