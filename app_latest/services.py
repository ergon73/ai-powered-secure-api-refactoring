"""
Business logic layer for user operations.

Provides thread-safe user management functions.
"""

import logging
import sqlite3
import threading
from typing import List, Optional, Dict, Any

from app_latest.database import get_db_connection


logger = logging.getLogger(__name__)

# Thread-safe active users tracking
_active_users: List[int] = []
_active_users_lock = threading.Lock()


def add_user(name: str, database_path: str) -> int:
    """
    Add new user to database with SQL injection protection.
    
    Args:
        name: User name (should be validated before calling).
        database_path: Path to database file.
        
    Returns:
        User ID of created user.
        
    Raises:
        sqlite3.IntegrityError: If user with same name already exists.
        sqlite3.Error: If database operation fails.
        ValueError: If name is invalid.
    """
    if not name or not isinstance(name, str):
        raise ValueError("Name must be a non-empty string")
    
    try:
        with get_db_connection(database_path) as conn:
            cursor = conn.execute(
                "INSERT INTO users (name) VALUES (?)",
                (name.strip(),)  # Parameterized query prevents SQL injection
            )
            user_id = cursor.lastrowid
            logger.info(f"User created with ID: {user_id}, name: {name[:20]}")
            return user_id
    except sqlite3.IntegrityError as e:
        logger.warning(f"Failed to create user (integrity error): {e}")
        raise
    except Exception as e:
        logger.error(f"Failed to create user: {e}", exc_info=True)
        raise


def get_user(user_id: int, database_path: str) -> Optional[Dict[str, Any]]:
    """
    Get user by ID safely.
    
    Args:
        user_id: User ID to retrieve.
        database_path: Path to database file.
        
    Returns:
        Dictionary with user data or None if not found.
        
    Raises:
        sqlite3.Error: If database operation fails.
    """
    if not isinstance(user_id, int) or user_id <= 0:
        return None
    
    try:
        with get_db_connection(database_path) as conn:
            cursor = conn.execute(
                "SELECT id, name FROM users WHERE id = ?",
                (user_id,)
            )
            row = cursor.fetchone()
            if row:
                return {"id": row["id"], "name": row["name"]}
            return None
    except sqlite3.Error as e:
        logger.error(f"Failed to get user {user_id}: {e}", exc_info=True)
        raise


def get_user_by_name(name: str, database_path: str) -> Optional[Dict[str, Any]]:
    """
    Get user by name safely.
    
    Args:
        name: User name to search for.
        database_path: Path to database file.
        
    Returns:
        Dictionary with user data or None if not found.
        
    Raises:
        sqlite3.Error: If database operation fails.
    """
    if not name or not isinstance(name, str):
        return None
    
    try:
        with get_db_connection(database_path) as conn:
            cursor = conn.execute(
                "SELECT id, name FROM users WHERE name = ?",
                (name.strip(),)
            )
            row = cursor.fetchone()
            if row:
                return {"id": row["id"], "name": row["name"]}
            return None
    except sqlite3.Error as e:
        logger.error(f"Failed to get user by name '{name}': {e}", exc_info=True)
        raise


def set_user_active(user_id: int) -> None:
    """
    Thread-safe active user tracking.
    
    Maintains list of up to 5 active users.
    
    Args:
        user_id: User ID to mark as active.
    """
    with _active_users_lock:
        if user_id not in _active_users:
            _active_users.append(user_id)
        if len(_active_users) > 5:
            _active_users.pop(0)


def get_active_users() -> List[int]:
    """
    Get list of active user IDs (thread-safe).
    
    Returns:
        List of active user IDs.
    """
    with _active_users_lock:
        return _active_users.copy()

