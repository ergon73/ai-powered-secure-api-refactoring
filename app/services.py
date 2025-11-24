"""
Business logic layer for user operations.

Provides thread-safe user management functions.
"""

import threading
from typing import List, Optional, Dict, Any

from app.database import get_db_connection


# Thread-safe active users tracking
_active_users: List[int] = []
_active_users_lock = threading.Lock()


def add_user(name: str) -> int:
    """
    Add new user to database with SQL injection protection.
    
    Args:
        name: User name.
        
    Returns:
        User ID of created user.
        
    Raises:
        sqlite3.Error: If database operation fails.
    """
    with get_db_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO users (name) VALUES (?)",
            (name,)  # Parameterized query prevents SQL injection
        )
        return cursor.lastrowid


def get_user(user_id: int) -> Optional[Dict[str, Any]]:
    """
    Get user by ID safely.
    
    Args:
        user_id: User ID to retrieve.
        
    Returns:
        Dictionary with user data or None if not found.
    """
    with get_db_connection() as conn:
        cursor = conn.execute(
            "SELECT id, name FROM users WHERE id = ?",
            (user_id,)
        )
        row = cursor.fetchone()
        if row:
            return {"id": row["id"], "name": row["name"]}
        return None


def get_user_by_name(name: str) -> Optional[Dict[str, Any]]:
    """
    Get user by name safely.
    
    Args:
        name: User name to search for.
        
    Returns:
        Dictionary with user data or None if not found.
    """
    with get_db_connection() as conn:
        cursor = conn.execute(
            "SELECT id, name FROM users WHERE name = ?",
            (name,)
        )
        row = cursor.fetchone()
        if row:
            return {"id": row["id"], "name": row["name"]}
        return None


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

