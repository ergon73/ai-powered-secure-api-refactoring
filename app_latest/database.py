"""
Database connection management and initialization.

Provides thread-safe database connection context manager.
"""

import sqlite3
import logging
from contextlib import contextmanager
from typing import Generator, Optional


logger = logging.getLogger(__name__)


@contextmanager
def get_db_connection(database_path: str) -> Generator[sqlite3.Connection, None, None]:
    """
    Thread-safe database connection context manager.
    
    Args:
        database_path: Path to SQLite database file.
    
    Yields:
        SQLite database connection.
        
    Raises:
        sqlite3.Error: If database operation fails.
    """
    conn: Optional[sqlite3.Connection] = None
    try:
        conn = sqlite3.connect(database_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        yield conn
        conn.commit()
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        logger.error(f"Database error: {e}", exc_info=True)
        raise
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Unexpected database error: {e}", exc_info=True)
        raise
    finally:
        if conn:
            conn.close()


def init_db(database_path: str) -> None:
    """
    Initialize database schema.
    
    Creates users table if it doesn't exist.
    Should be called once before starting the application,
    not in each worker process.
    
    Args:
        database_path: Path to SQLite database file.
    """
    try:
        with get_db_connection(database_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    password_hash TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            logger.info(f"Database initialized at {database_path}")
    except sqlite3.Error as e:
        logger.error(f"Failed to initialize database: {e}", exc_info=True)
        raise

