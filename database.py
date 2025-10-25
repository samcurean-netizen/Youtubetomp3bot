import sqlite3
import logging
import asyncio
from contextlib import contextmanager
from typing import Optional, Set, Any
from functools import wraps

logger = logging.getLogger(__name__)

DB_PATH = "bot_data.db"

_db_lock = asyncio.Lock()

def async_db_operation(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with _db_lock:
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, lambda: func(*args, **kwargs))
    return wrapper

@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        logger.error(f"Database error: {e}")
        raise
    finally:
        conn.close()

def init_database():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chat_settings (
                chat_id INTEGER PRIMARY KEY,
                delete_after_transcription INTEGER DEFAULT 1,
                admin_prompted INTEGER DEFAULT 0
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS processed_messages (
                chat_id INTEGER,
                message_id INTEGER,
                PRIMARY KEY (chat_id, message_id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS processed_audio_ids (
                audio_file_id TEXT PRIMARY KEY,
                processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        logger.info("Database initialized successfully")

@async_db_operation
def get_chat_setting(chat_id: int, setting_name: str, default: Any = None) -> Any:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT {setting_name} FROM chat_settings WHERE chat_id = ?",
            (chat_id,)
        )
        row = cursor.fetchone()
        if row is None:
            return default
        return row[0]

@async_db_operation
def set_chat_setting(chat_id: int, setting_name: str, value: Any):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO chat_settings (chat_id) VALUES (?)",
            (chat_id,)
        )
        cursor.execute(
            f"UPDATE chat_settings SET {setting_name} = ? WHERE chat_id = ?",
            (value, chat_id)
        )
        logger.info(f"Chat {chat_id}: Set {setting_name} to {value}")

async def get_delete_after_transcription(chat_id: int) -> bool:
    result = await get_chat_setting(chat_id, "delete_after_transcription", default=1)
    return bool(result)

async def set_delete_after_transcription(chat_id: int, delete: bool):
    await set_chat_setting(chat_id, "delete_after_transcription", 1 if delete else 0)

async def get_admin_prompted(chat_id: int) -> bool:
    result = await get_chat_setting(chat_id, "admin_prompted", default=0)
    return bool(result)

async def set_admin_prompted(chat_id: int, prompted: bool):
    await set_chat_setting(chat_id, "admin_prompted", 1 if prompted else 0)

@async_db_operation
def is_message_processed(chat_id: int, message_id: int) -> bool:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT 1 FROM processed_messages WHERE chat_id = ? AND message_id = ?",
            (chat_id, message_id)
        )
        return cursor.fetchone() is not None

@async_db_operation
def mark_message_processed(chat_id: int, message_id: int):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO processed_messages (chat_id, message_id) VALUES (?, ?)",
            (chat_id, message_id)
        )
        logger.debug(f"Marked message {message_id} in chat {chat_id} as processed")

@async_db_operation
def is_audio_processed(audio_file_id: str) -> bool:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT 1 FROM processed_audio_ids WHERE audio_file_id = ?",
            (audio_file_id,)
        )
        return cursor.fetchone() is not None

@async_db_operation
def mark_audio_processed(audio_file_id: str):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO processed_audio_ids (audio_file_id) VALUES (?)",
            (audio_file_id,)
        )
        logger.debug(f"Marked audio {audio_file_id} as processed")

@async_db_operation
def get_all_chat_ids() -> Set[int]:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT chat_id FROM chat_settings")
        return {row[0] for row in cursor.fetchall()}
