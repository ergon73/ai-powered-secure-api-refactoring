"""
Database connection management and initialization.

Provides thread-safe database connection context manager.
"""

import sqlite3
from contextlib import contextmanager
from typing import Generator


DATABASE_PATH = "secure_app.db"


@contextmanager
def get_db_connection() -> Generator[sqlite3.Connection, None, None]:
    """
    Thread-safe database connection context manager.
    
    Yields:
        SQLite database connection.
        
    Raises:
        sqlite3.Error: If database operation fails.
    """
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db() -> None:
    """
    Initialize database schema.
    
    Creates users table if it doesn't exist.
    """
    with get_db_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                password_hash TEXT
            )
        """)

