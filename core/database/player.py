import asyncpg
from core.database.Database import DatabaseTable, SCHEMA


class PlayerTable(DatabaseTable):
    """
    Handles player_info table operations.
    Works with tg_identity table to map Telegram user IDs to internal user IDs.
    """
    
    def __init__(self, pool: asyncpg.Pool, telegram_user_id: int):
        """
        Initialize PlayerTable with Telegram user ID.
        
        Args:
            pool: Database connection pool
            telegram_user_id: Telegram user ID (from message.from_user.id)
        """
        super().__init__(pool)
        self.TABLE_NAME = f"{SCHEMA}.player_info"
        self.TG_IDENTITY_TABLE = f"{SCHEMA}.tg_identity"

        self.CHARACTER_NAME = "character_name"
        self.LANGUAGE = "language"

        self.telegram_user_id = telegram_user_id
        self._internal_user_id: int | None = None

    async def _get_or_create_internal_user_id(self) -> int:
        """
        Get or create internal user_id from tg_identity table.
        Setup internal user_id if not exists.
        Returns the internal user_id that references tg_identity.
        """
        if self._internal_user_id is not None:
            return self._internal_user_id

        async with self.pool.acquire() as connection:
            # Try to get existing user_id
            user_id = await connection.fetchval(
                f"""
                SELECT user_id 
                FROM {self.TG_IDENTITY_TABLE} 
                WHERE telegram_user_id = $1;
                """,
                self.telegram_user_id
            )

            if user_id is None:
                # Create new entry in tg_identity
                user_id = await connection.fetchval(
                    f"""
                    INSERT INTO {self.TG_IDENTITY_TABLE} (telegram_user_id) 
                    VALUES ($1) 
                    ON CONFLICT (telegram_user_id) DO UPDATE 
                    SET telegram_user_id = EXCLUDED.telegram_user_id 
                    RETURNING user_id;
                    """,
                    self.telegram_user_id
                )
                self.logger.debug("Created new tg_identity entry for telegram_user_id=%i, user_id=%i", 
                                self.telegram_user_id, user_id)
            else:
                self.logger.debug("Found existing tg_identity for telegram_user_id=%i, user_id=%i", 
                                self.telegram_user_id, user_id)

            self._internal_user_id = user_id
            return user_id

    async def player_exists(self) -> bool:
        """
        Check if player exists in player_info table.
        Uses the internal user_id from tg_identity.
        """
        internal_user_id = await self._get_or_create_internal_user_id()
        async with self.pool.acquire() as connection:
            exists = await connection.fetchval(
                f"""
                SELECT EXISTS (
                SELECT 1 
                FROM {self.TABLE_NAME} 
                WHERE {self.KEY} = $1
                );
                """,
                internal_user_id
            )
            return bool(exists)

    async def create_character(self, name: str | None, language: str) -> None:
        """
        Create a new character in player_info table.
        Ensures tg_identity entry exists first.
        """
        internal_user_id = await self._get_or_create_internal_user_id()
        
        async with self.pool.acquire() as connection:
            # Update updated_at timestamp on insert
            status = await connection.execute(
                f"""
                INSERT INTO {self.TABLE_NAME}
                    ({self.KEY}, {self.CHARACTER_NAME}, {self.LANGUAGE}, updated_at) 
                    VALUES ($1, $2, $3, CURRENT_TIMESTAMP) 
                    ON CONFLICT ({self.KEY}) DO UPDATE SET 
                        {self.CHARACTER_NAME} = COALESCE(
                            EXCLUDED.{self.CHARACTER_NAME}, 
                            {self.TABLE_NAME}.{self.CHARACTER_NAME}
                        ), 
                        {self.LANGUAGE} = COALESCE(
                            EXCLUDED.{self.LANGUAGE}, 
                            {self.TABLE_NAME}.{self.LANGUAGE}
                        ), 
                        updated_at = CURRENT_TIMESTAMP;
                        """,
                internal_user_id, name, language
            )
            self.logger.debug("TRANSACTION_STATUS character creation: %s", status)

    async def get_character_name(self) -> str | None:
        """Get character name for the player."""
        internal_user_id = await self._get_or_create_internal_user_id()
        return await self._get_element(key=internal_user_id, attribute=self.CHARACTER_NAME)

    async def get_language(self) -> str:
        """Get language preference for the player."""
        internal_user_id = await self._get_or_create_internal_user_id()
        language = await self._get_element(key=internal_user_id, attribute=self.LANGUAGE)
        if not language:
            return 'en'
        return language

    async def set_character_name(self, name: str) -> None:
        """Update character name and updated_at timestamp."""
        internal_user_id = await self._get_or_create_internal_user_id()
        async with self.pool.acquire() as connection:
            await connection.execute(
                f"""
                UPDATE {self.TABLE_NAME} 
                SET {self.CHARACTER_NAME} = $1, 
                    updated_at = CURRENT_TIMESTAMP 
                WHERE {self.KEY} = $2;
                """,
                name, internal_user_id
            )

    async def set_language(self, language: str) -> None:
        """Update language preference and updated_at timestamp."""
        internal_user_id = await self._get_or_create_internal_user_id()
        async with self.pool.acquire() as connection:
            await connection.execute(
                f"""
                UPDATE {self.TABLE_NAME} 
                SET {self.LANGUAGE} = $1, 
                    updated_at = CURRENT_TIMESTAMP 
                WHERE {self.KEY} = $2;
                """,
                language, internal_user_id
            )

    