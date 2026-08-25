import logging
from typing import List, Tuple
import aiosqlite
import config

logger = logging.getLogger(__name__)

async def setup_db(db_path: str = config.DATABASE_PATH) -> None:
    """Initializes the database and creates necessary tables if they do not exist."""
    try:
        async with aiosqlite.connect(db_path) as db:
            await db.execute("""
                CREATE TABLE IF NOT EXISTS voice_states (
                    guild_id INTEGER PRIMARY KEY,
                    channel_id INTEGER NOT NULL
                )
            """)
            await db.commit()
            logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to setup database: {e}")
        raise

async def save_state(guild_id: int, channel_id: int, db_path: str = config.DATABASE_PATH) -> None:
    """Saves or updates a guild's voice channel state."""
    try:
        async with aiosqlite.connect(db_path) as db:
            await db.execute(
                "REPLACE INTO voice_states (guild_id, channel_id) VALUES (?, ?)",
                (guild_id, channel_id)
            )
            await db.commit()
    except Exception as e:
        logger.error(f"Error saving voice state for guild {guild_id}: {e}")

async def remove_state(guild_id: int, db_path: str = config.DATABASE_PATH) -> None:
    """Removes a guild's voice state from the database."""
    try:
        async with aiosqlite.connect(db_path) as db:
            await db.execute("DELETE FROM voice_states WHERE guild_id = ?", (guild_id,))
            await db.commit()
    except Exception as e:
        logger.error(f"Error removing voice state for guild {guild_id}: {e}")

async def get_saved_channels(db_path: str = config.DATABASE_PATH, limit: int = 200) -> List[Tuple[int, int]]:
    """Retrieves all active voice channel states for auto-reconnection on startup."""
    channels: List[Tuple[int, int]] = []
    try:
        async with aiosqlite.connect(db_path) as db:
            async with db.execute("SELECT guild_id, channel_id FROM voice_states LIMIT ?", (limit,)) as cursor:
                async for row in cursor:
                    channels.append((row[0], row[1]))
    except Exception as e:
        logger.error(f"Error fetching saved voice channels: {e}")
    return channels
