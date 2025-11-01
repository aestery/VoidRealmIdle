import psycopg2
from psycopg2._psycopg import cursor
import asyncpg
from decouple import config


class DatabaseHandle():
    def __init__(self, dataBaseURL, isAsync=True) -> None:
        self._dataBaseURL = dataBaseURL

        if isAsync:
            pass
        else:
            self._connection = psycopg2.connect(dataBaseURL)
    
    async def create_pool(self, minConnections=1, maxConnections=10) -> asyncpg.Pool:
        return await asyncpg.create_pool(
            dsn=self._dataBaseURL,
            min_size=minConnections,
            max_size=maxConnections
        )
    
    def CreatePsycopgCursor(self) -> cursor:
        return self._connection.cursor()
    