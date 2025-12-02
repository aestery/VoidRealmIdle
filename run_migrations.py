"""
Standalone script to run database migrations.
Can be executed independently or via Docker Compose.
"""
import asyncio
import logging
import sys
from decouple import config

from core.database.Database import DatabaseHandle, SCHEMA
from core.database.migrations.migration_runner import MigrationRunner


async def main():
    """Run all pending database migrations."""
    # Setup basic logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    try:
        db_url = config('DB_URL')
        logger.info("Connecting to database...")
        
        database = DatabaseHandle(db_url)
        pool = await database.create_pool()
        
        logger.info("Running database migrations...")
        migration_runner = MigrationRunner(pool, schema=SCHEMA)
        await migration_runner.run_all_pending()
        
        logger.info("All migrations completed successfully")
        await pool.close()
        sys.exit(0)
        
    except Exception as e:
        logger.error(f"Migration failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

