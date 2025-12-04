"""
Pure SQL migration runner for database schema management.
Tracks applied migrations in a migrations table.
"""
import asyncpg
import logging
from pathlib import Path
from typing import List, Tuple
from core.game_objects.items.item import ItemRegistry


class MigrationRunner:
    """Handles running SQL migrations and tracking their status."""
    
    def __init__(self, pool: asyncpg.Pool, schema: str = "test"):
        self.pool = pool
        self.schema = schema
        self.logger = logging.getLogger(__name__)
        self.migrations_dir = Path(__file__).parent / "sql"
        self.migrations_table = f"{schema}.migrations"
    
    async def ensure_migrations_table(self) -> None:
        """Create the migrations tracking table if it doesn't exist."""
        async with self.pool.acquire() as conn:
            # Ensure schema exists
            await conn.execute(f"""CREATE SCHEMA IF NOT EXISTS {self.schema};""")
            
            # Create migrations table
            await conn.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.migrations_table} (
                    id SERIAL PRIMARY KEY,
                    filename VARCHAR(255) NOT NULL UNIQUE,
                    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    checksum VARCHAR(64)
                );
            """)
            self.logger.info(f"Migrations table ensured: {self.migrations_table}")
    
    async def get_applied_migrations(self) -> List[str]:
        """Get list of already applied migration filenames."""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                f"""SELECT filename 
                    FROM {self.migrations_table} 
                    ORDER BY id;"""
            )
            return [row['filename'] for row in rows]
    
    def get_migration_files(self) -> List[Tuple[str, Path]]:
        """Get all SQL migration files sorted by name."""
        if not self.migrations_dir.exists():
            self.logger.warning(f"Migrations directory not found: {self.migrations_dir}")
            return []
        
        sql_files = sorted(self.migrations_dir.glob("*.sql"))
        return [(f.name, f) for f in sql_files]
    
    def _is_empty_sql(self, sql_content: str) -> bool:
        """Check if SQL content is empty or contains only comments/whitespace."""
        # Remove comments and whitespace
        lines = sql_content.split('\n')
        sql_lines = []
        for line in lines:
            stripped = line.strip()
            # Skip empty lines and comment-only lines
            if stripped and not stripped.startswith('--'):
                sql_lines.append(stripped)
        return len(sql_lines) == 0
    
    async def run_migration(self, filename: str, filepath: Path) -> None:
        """Execute a single migration file."""
        self.logger.info(f"Running migration: {filename}")
        
        async with self.pool.acquire() as conn:
            async with conn.transaction():
                # Read SQL file
                sql_content = filepath.read_text(encoding='utf-8')
                
                # Skip empty or comment-only migrations
                if self._is_empty_sql(sql_content):
                    self.logger.info(f"Skipping empty migration file: {filename}")
                    # Still record it as applied
                    await conn.execute(
                        f"""INSERT INTO {self.migrations_table} (filename) 
                            VALUES ($1);""",
                        filename
                    )
                    return
                
                # Execute migration
                await conn.execute(sql_content)
                
                # Record migration
                await conn.execute(
                    f"""
                    INSERT INTO {self.migrations_table} (filename) 
                    VALUES ($1);
                    """,
                    filename
                )
                
                self.logger.info(f"Migration applied successfully: {filename}")
    
    async def populate_item_relation(self) -> None:
        """Populate item relation mapping after migrations."""
        async with self.pool.acquire() as conn:
            items = ItemRegistry.get_all_items()

            for item_id, item in items.items():
                
                await conn.execute(
                    f"""
                    INSERT INTO {self.schema}.items (item_id)
                    VALUES ($1)
                    ON CONFLICT (item_id) DO NOTHING; 
                    """,
                    item_id
                )
                self.logger.debug(f"Item ID {item_id} populated in items table.")

        self.logger.info("Item relation mapping populated.")

    async def run_all_pending(self) -> None:
        """Run all pending migrations in order."""
        await self.ensure_migrations_table()
        
        applied = set[str](await self.get_applied_migrations())
        migrations = self.get_migration_files()
        
        pending = [(name, path) for name, path in migrations if name not in applied]
        
        if not pending:
            self.logger.info("No pending migrations found")
            return
        
        self.logger.info(f"Found {len(pending)} pending migration(s)")
        
        for filename, filepath in pending:
            try:
                await self.run_migration(filename, filepath)
            except Exception as e:
                self.logger.error(f"Failed to apply migration {filename}: {e}")
                raise
        
        # After all migrations, populate item relation mapping
        try:
            await self.populate_item_relation()
        except Exception as e:
            self.logger.error(f"Failed to populate item relation mapping: {e}")
            raise

